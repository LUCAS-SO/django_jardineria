# Jardinería App — Gestión de Trabajos

Aplicación web desarrollada en **Django** para registrar, organizar y reportar trabajos de mantenimiento de espacios verdes.

Pensada como **herramienta interna** para cuadrillas o prestadores de servicios.

---

## ¿Qué hace?

- Registra trabajos realizados (fecha, descripción, duración)
- Asocia fotos *antes / después*
- Etiqueta trabajos por tipo de tarea
- Exporta reportes en **PDF** y **Excel**
- Administra todo desde el **panel de Django**
- Incluye **pantalla de carga (splash)** para servidores con cold start

---

## Stack Tecnológico

- **Backend:** Python / Django
- **Frontend:** HTML + Tailwind (mobile first)
- **Base de datos:** SQLite (local) / PostgreSQL (producción)
- **Imágenes:** Cloudinary
- **Deploy:** Render (plataformas cloud)
- **Seguridad:** Middleware propio + HTTPS + rate limiting

---

## Features Técnicas Destacadas

- Configuración separada por entorno (`local / production`)
- Exportación automática de reportes (PDF/XLSX)
- Healthcheck para monitoreo y cold start handling
- Splash screen minimalista con estado del servidor
- Middleware custom contra bots y abuso
- Arquitectura simple, reutilizable y extensible

---

## Caso de uso real

> Registrar trabajos diarios, documentar resultados con fotos  
> y entregar reportes claros a clientes o empresas.

---

## Estado

Proyecto funcional — usado como **base**, no demo.

---

## Autor

Lucas Soria
Desarrollador Web · Django

