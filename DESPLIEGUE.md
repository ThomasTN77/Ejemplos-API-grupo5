# Guía de despliegue — Entrega final

Fecha límite: sábado 21 de noviembre de 2026.

## 1. Backend en Render

El archivo `render.yaml` define dos servicios gratuitos:

| Servicio | Carpeta | Base de datos |
|---|---|---|
| `api-videojuegos-grupo5` | `Maria/` | Neon (misma que en local) |
| `api-animales-grupo5` | `Thomas/` | Neon (misma que en local) |
| `api-libros-grupo5` | `Mauricio/` | Neon (misma que en local) |
| `api-motos-grupo5` | `Juanda/` | Neon (misma que en local) |

Pasos:

1. Crear cuenta en https://render.com (se puede entrar con GitHub).
2. **New → Blueprint** y conectar el repositorio `Maria-0922/Ejemplos-API-grupo5`.
3. Render detectará `render.yaml` y pedirá los valores de `DATABASE_URL` (`sync: false`).
   Pegar en los cuatro servicios la cadena que está en `Maria/.env`:
   ```
   postgresql://neondb_owner:...@ep-noisy-rain-.../neondb?sslmode=require
   ```
4. Esperar a que ambos servicios digan **Live** (puede tardar 5-10 min la primera vez).
5. Copiar las URLs que terminen en `.onrender.com` de los cuatro servicios.

Comprobar: abrir `https://<servicio>.onrender.com/docs`. Debe cargar Swagger.

> En el plan gratuito Render duerme el servicio tras ~15 min sin uso;
> la primera petición después de eso tarda ~30 s en responder. Es normal.

## 2. Actualizar las URLs del frontend

Editar `Frontend-GRUPO5-A-SW/src/environments/environment.ts` con las URLs reales:

```ts
export const environment = {
  apiUrl: 'https://URL-DEL-SERVICIO-ANIMALES.onrender.com',
  videojuegosApiUrl: 'https://URL-DEL-SERVICIO-VIDEOJUEGOS.onrender.com',
  librosApiUrl: 'https://URL-DEL-SERVICIO-LIBROS.onrender.com',
  motosApiUrl: 'https://URL-DEL-SERVICIO-MOTOS.onrender.com',
};
```

Luego:

```powershell
cd Frontend-GRUPO5-A-SW
npm run build
```

## 3. Frontend en Firebase Hosting

1. Crear un proyecto en https://console.firebase.google.com (plan Spark, gratis).
2. Instalar la CLI (si no está): `npm install -g firebase-tools`
3. Iniciar sesión: `firebase login`
4. Seleccionar el proyecto: `firebase use --add` (elegir el proyecto creado).
5. Desplegar: `firebase deploy --only hosting`

El archivo `firebase.json` ya está configurado:
- `public`: `dist/frontend/browser`
- `rewrites`: todas las rutas → `index.html` (necesario para Angular)

Firebase mostrará la URL final: `https://<proyecto>.web.app`

## 4. Verificación final

Abrir la URL de Firebase y comprobar:

- [ ] `/inicio` carga
- [ ] `/animales` lista datos del backend de Render
- [ ] `/videojuegos` muestra "Conectado" y lista datos del backend de Render
- [ ] `/libros` lista datos del backend de Render
- [ ] `/motos` lista datos del backend de Render
- [ ] Se puede crear, editar, eliminar y buscar por ID
- [ ] `https://<backend>.onrender.com/docs` responde

## 5. URLs finales de esta entrega

Frontend: https://grupo5-api-frontend.web.app

Backends:

| Servicio | URL |
|---|---|
| Videojuegos | https://api-videojuegos-grupo5.onrender.com |
| Animales | https://api-animales-grupo5.onrender.com |
| Libros | https://api-libros-grupo5.onrender.com |
| Motos | https://api-motos-grupo5.onrender.com |

Entregar: **la URL `https://grupo5-api-frontend.web.app`** (mencionando también las URLs de los backends).
