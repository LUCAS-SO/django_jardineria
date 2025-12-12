from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Job

# Exportar a Excel / CSV
import csv
from django.http import HttpResponse
from openpyxl import Workbook
from datetime import datetime

# Exportar a PDF
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


# ==============================
# Helpers
# ==============================

def format_minutes(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return hours, minutes


# Diccionario para traducir meses al español
MESES_ES = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre"
}


# ==============================
# VISTAS WEB
# ==============================

class JobListView(ListView):
    model = Job
    template_name = 'job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Agrupación mensual
        monthly_totals = (
            Job.objects
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total_minutes=Sum('duration'))
            .order_by('-month')
        )

        for item in monthly_totals:
            hours, minutes = format_minutes(item["total_minutes"])
            item["hours"] = hours
            item["minutes"] = minutes

        context['monthly_totals'] = monthly_totals
        return context


class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.object

        hours, minutes = format_minutes(self.object.duration)
        context["duration_hours"] = hours
        context["duration_minutes"] = minutes

        context["has_before"] = job.photos.filter(before_after='before').exists()
        context["has_after"] = job.photos.filter(before_after='after').exists()
        context["has_both"] = (
            context["has_before"] and context["has_after"]
        )

        return context


# ==============================
# EXPORTAR CSV
# ==============================

def export_jobs_csv(request):
    response = HttpResponse(content_type='text/csv')
    filename = f"trabajos_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Locación', 'Duración (min)', 'Descripción'])

    for job in Job.objects.order_by('-date'):
        writer.writerow([
            job.date,
            job.get_location_display(),
            job.duration,
            job.description,
        ])

    return response


# ==============================
# EXPORTAR XLSX
# ==============================

def export_jobs_xlsx(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Trabajos"

    ws.append(['Fecha', 'Locación', 'Duración (min)', 'Duración (hh:mm)', 'Descripción'])

    total_minutos = 0

    def minutos_a_horas(mins):
        horas = mins // 60
        minutos = mins % 60
        return f"{horas}h {minutos:02d}m"

    for job in Job.objects.order_by('-date'):
        ws.append([
            job.date.strftime("%Y-%m-%d"),
            job.get_location_display(),
            job.duration,
            minutos_a_horas(job.duration),
            job.description,
        ])
        total_minutos += job.duration

    ws.append([])
    ws.append(["","TOTAL", f"{total_minutos}m", minutos_a_horas(total_minutos),""])

    # Estilo para el total
    from openpyxl.styles import Font
    total_row = ws.max_row
    ws[f"B{total_row}"].font = Font(bold=True)
    ws[f"C{total_row}"].font = Font(bold=True)
    ws[f"D{total_row}"].font = Font(bold=True)

    # Respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"trabajos_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    wb.save(response)
    return response


# ==============================
# EXPORTAR PDF
# ==============================

def export_jobs_pdf(request):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Título
    title = Paragraph("Reporte de Trabajos - Lucas Soria", styles["Title"])
    elements.append(title)
    elements.append(Paragraph("<br/>", styles["Normal"]))

    # Obtener trabajos
    jobs = Job.objects.all().order_by("-date")

    # Construir tabla
    data = [["Fecha", "Descripción", "Duración"]]

    total_minutes_all = 0

    for job in jobs:
        desc = job.description or "N/A"
        dur = int(job.duration) if job.duration else 0
        total_minutes_all += dur

        data.append([
            job.date.strftime("%d/%m/%Y"),
            desc,
            f"{dur // 60}h {dur % 60}m"
        ])

    # Estilo de tabla
    table = Table(data, colWidths=[80, 300, 80])
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#045C7C")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ])
    table.setStyle(table_style)
    elements.append(table)

    # Totales Mensuales
    monthly_totals = (
        Job.objects
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total_minutes=Sum("duration"))
        .order_by("-month")
    )

    if monthly_totals:
        elements.append(Paragraph("<br/>", styles["Normal"]))
        elements.append(Paragraph("<b>Totales Mensuales</b>", styles["Heading2"]))
        elements.append(Paragraph("<br/>", styles["Normal"]))

        for item in monthly_totals:
            month = item["month"]
            total_minutes = item["total_minutes"] or 0

            hours = total_minutes // 60
            minutes = total_minutes % 60

            # Traducción manual del mes
            mes_en = month.strftime("%B")
            mes_es = MESES_ES.get(mes_en, mes_en)
            month_str = f"{mes_es} {month.strftime('%Y')}"

            elements.append(
                Paragraph(f"<b>{month_str}:</b> {hours}h {minutes}m", styles["Normal"])
            )

    # Total General
    if total_minutes_all > 0:
        h = total_minutes_all // 60
        m = total_minutes_all % 60

        elements.append(Paragraph("<br/>", styles["Normal"]))
        elements.append(
            Paragraph(
            f"<b>Total General:</b> {h}h {m:02d}m",
            styles["Heading2"]
            )
        )

    # Construir PDF
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="trabajos_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
    )

    return response