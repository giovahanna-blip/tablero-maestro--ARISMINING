import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk

st.set_page_config(page_title="Tablero ASG Aris Mining", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# ESTILOS CSS GLOBALES
# ==========================================
estilos = '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&display=swap');
html, body, [class*="css"], .stMarkdown, .stText { font-family: 'Montserrat', sans-serif !important; }

/* Contenedores KPI Globales */
.kpi-container { display: flex; justify-content: space-between; gap: 20px; margin-bottom: 25px; align-items: flex-start; flex-wrap: wrap; }
.kpi-card { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 25px 15px; flex: 1; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.3s ease, box-shadow 0.3s ease; min-width: 180px; }
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 10px 15px rgba(0,0,0,0.1); border-color: #1E3A8A; }
.kpi-title { font-size: 1.05em; color: #374151; margin-bottom: 10px; font-weight: 500; }
.kpi-value { font-size: 3.5em; font-weight: 700; color: #1E3A8A; margin: 0; line-height: 1.1; }
.kpi-delta { font-size: 0.95em; margin-top: 15px; padding: 8px 16px; border-radius: 20px; display: inline-block; font-weight: 700; border: 1px solid #bbf7d0; background-color: #d1fae5; color: #065f46;}

/* Estilos Balanza Social */
.panel-base { border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); padding: 0 0 15px 0; background: white; border: 1px solid #e5e7eb; height: 100%; overflow: hidden;}
.header-verde { background-color: #00a651; color: white; padding: 10px 15px; font-weight: 800; font-size: 1.1rem; display: flex; align-items: center; gap: 10px;}
.header-amarillo { background-color: #fdb913; color: white; padding: 10px 15px; font-weight: 800; font-size: 1.1rem; display: flex; align-items: center; gap: 10px;}
.header-rojo { background-color: #ed1c24; color: white; padding: 10px 15px; font-weight: 800; font-size: 1.1rem; display: flex; align-items: center; gap: 10px;}

.tarjetas-container { display: flex; justify-content: space-around; padding: 15px; gap: 12px; flex-wrap: wrap;}
details.tarjeta-btn { flex: 1; min-width: 130px; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 12px 8px; text-align: center; transition: all 0.2s ease-in-out; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.03); }
details.tarjeta-btn.verde { border-bottom: 4px solid #00a651; }
details.tarjeta-btn.amarillo { border-bottom: 4px solid #fdb913; }
details.tarjeta-btn.rojo { border-bottom: 4px solid #ed1c24; }
details.tarjeta-btn.gi { border-left: 4px solid #0087a3; text-align: left; margin-bottom: 10px; }
details.tarjeta-btn:hover { transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.08); }
details.tarjeta-btn summary { list-style: none; outline: none; }
details.tarjeta-btn summary::-webkit-details-marker { display: none; }

.t-icono { font-size: 2rem; margin-bottom: 5px; color: #374151;}
.t-titulo { font-weight: 700; font-size: 0.85rem; margin-bottom: 5px; color: #1f2937; line-height: 1.2;}
.t-presion { color: #ed1c24; font-weight: 800; font-size: 0.8rem; margin-bottom: 5px;}
.t-porcentaje-verde { color: #00a651; font-weight: 800; font-size: 2rem; line-height: 1;}
.t-porcentaje-rojo { color: #ed1c24; font-weight: 800; font-size: 2rem; line-height: 1;}

.click-hint { font-size: 0.65rem; color: #6b7280; margin-top: 6px; font-weight: 600; background: #f3f4f6; border-radius: 10px; padding: 2px 6px; display: inline-block;}
details.tarjeta-btn[open] .click-hint { display: none; }
.expanded-content { margin-top: 10px; padding-top: 10px; border-top: 1px dashed #d1d5db; font-size: 0.8rem; color: #4b5563; font-weight: 600; line-height: 1.3; }

/* Botones KPI Ambientales Interactivos */
details.kpi-btn { flex: 1; min-width: 140px; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 15px 10px; text-align: center; transition: all 0.2s ease-in-out; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.03); }
details.kpi-btn:hover { transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.08); border-color: #10b981; }
details.kpi-btn summary { list-style: none; outline: none; }
details.kpi-btn summary::-webkit-details-marker { display: none; }
.kpi-btn-title { font-size: 0.95rem; color: #4b5563; margin-bottom: 5px; font-weight: 600; }
.kpi-btn-value { font-size: 2rem; font-weight: 800; color: #1e3a8a; margin: 10px 0; line-height: 1.1; }
.kpi-btn-delta { font-size: 0.85rem; padding: 5px 12px; border-radius: 20px; display: inline-block; font-weight: 700; background-color: #d1fae5; color: #065f46;}
.click-hint-kpi { font-size: 0.75rem; color: #6b7280; margin-top: 10px; font-weight: 600; background: #f3f4f6; border-radius: 10px; padding: 3px 8px; display: inline-block;}
details.kpi-btn[open] .click-hint-kpi { display: none; }
.expanded-content-kpi { margin-top: 12px; padding-top: 10px; border-top: 1px dashed #d1d5db; font-size: 0.82rem; color: #374151; font-weight: 500; line-height: 1.4; text-align: left; }

.panel-kpi { background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 20px; text-align: center; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;}
.circulo-kpi { border: 5px solid #00a651; border-radius: 50%; width: 95px; height: 90px; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; font-weight: 800; color: #00a651; margin-bottom: 12px; background: white;}
.desc-kpi { font-size: 0.85rem; color: #065f46; font-weight: 600;}

.gi-titulo { font-weight: 800; color: #1f2937; font-size: 1rem; border-bottom: 3px solid #0087a3; padding-bottom: 5px; margin-bottom: 15px;}
.friccion-content { padding: 15px; display: flex; flex-direction: column; gap: 15px; }
.actor-card { border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.2s ease; }
.actor-card:hover { transform: scale(1.01); }

/* Estructura Infográfica Universal para Pilares 3, 4 y 5 */
.rel-main-container { display: flex; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 15px; border: 1px solid #e5e7eb; min-height: 400px;}
.rel-left { color: white; padding: 30px; flex: 1; min-width: 280px; max-width: 320px; display: flex; flex-direction: column; justify-content: center;}
.rel-left h2 { font-weight: 800; font-size: 1.8rem; line-height: 1.2; margin-bottom: 15px; color: white; }
.rel-left p { font-size: 0.95rem; line-height: 1.5; color: rgba(255,255,255,0.9);}
.rel-left blockquote { font-style: italic; font-weight: 600; border-left: 4px solid rgba(255,255,255,0.6); padding-left: 15px; margin-top: 25px; color: rgba(255,255,255,0.95);}
.rel-right { background: #ffffff; flex: 2.5; padding: 30px; display: flex; flex-direction: column; justify-content: center;}

.rel-obj-container { display: flex; gap: 15px; margin-bottom: 25px; flex-wrap: wrap;}
.rel-obj { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; flex: 1; text-align: center; min-width: 130px;}
.rel-obj-num { width: 30px; height: 30px; border-radius: 50%; background: #3b82f6; color: white; font-weight: bold; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto; }
.rel-obj-title { font-weight: 700; font-size: 0.9rem; color: #1e3a8a; margin-bottom: 5px;}
.rel-obj-desc { font-size: 0.8rem; color: #64748b; line-height: 1.3;}

.mech-details { margin-bottom: 10px; background: #ffffff; border-radius: 8px; border: 1px solid #e2e8f0; cursor: pointer; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.02);}
.mech-details:hover { border-color: #3b82f6; background: #f8fafc; box-shadow: 0 4px 8px rgba(0,0,0,0.06);}
.mech-details summary { display: flex; align-items: center; padding: 12px 15px; outline: none; list-style: none; font-weight: 800; color: #1e3a8a; font-size: 1rem;}
.mech-details summary::-webkit-details-marker { display: none; }
.mech-num { width: 32px; height: 32px; border-radius: 50%; color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; margin-right: 15px; font-size: 1rem; flex-shrink: 0;}
.mech-icon { font-size: 1.4rem; margin-right: 15px; flex-shrink: 0;}
.mech-desc { padding: 15px 15px 15px 62px; font-size: 0.9rem; color: #334155; border-top: 1px dashed #cbd5e1; background: #f8fafc; border-radius: 0 0 8px 8px; line-height: 1.5; font-weight: 500;}

/* ========================================================
   ESTILOS EXCLUSIVOS: INFOGRAFÍA PESTAÑA INICIO
   ======================================================== */
.macro-container {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    padding: 40px; border-radius: 15px; box-shadow: inset 0 0 20px rgba(0,0,0,0.05); margin-bottom: 30px;
}
.header-info { text-align: center; margin-bottom: 50px; }
.header-info h1 { font-size: 3rem; color: #1e3a8a; font-weight: 800; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.05); }
.header-info p { font-size: 1.3rem; color: #334155; font-weight: 600; font-style: italic; background: #e0e7ff; display: inline-block; padding: 8px 20px; border-radius: 30px; }

/* Grid de la infografía */
.grid-infra {
    display: grid; grid-template-columns: 1fr 340px 1fr; grid-template-rows: auto auto; gap: 25px; align-items: center; position: relative;
}

/* Donut Chart Central con CSS Puro */
.donut-wrapper {
    grid-column: 2; grid-row: 1 / 3; display: flex; justify-content: center; align-items: center; position: relative; margin: 20px 0;
}
.donut-chart {
    position: relative; width: 320px; height: 320px; border-radius: 50%;
    background: conic-gradient(from 324deg,
        #3b82f6 0deg 68deg, transparent 68deg 72deg,
        #ef4444 72deg 140deg, transparent 140deg 144deg,
        #4338ca 144deg 212deg, transparent 212deg 216deg,
        #f59e0b 216deg 284deg, transparent 284deg 288deg,
        #10b981 288deg 356deg, transparent 356deg 360deg
    );
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    transition: transform 0.4s ease;
}
.donut-chart:hover { transform: scale(1.03); box-shadow: 0 15px 35px rgba(0,0,0,0.15); }
.donut-inner {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    width: 190px; height: 190px; background: white; border-radius: 50%;
    display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;
    box-shadow: inset 0 4px 10px rgba(0,0,0,0.05); z-index: 10;
}
.d-icon {
    position: absolute; width: 45px; height: 45px; border-radius: 50%; background: white;
    display: flex; justify-content: center; align-items: center; font-size: 1.4rem; font-weight: bold;
    box-shadow: 0 4px 6px rgba(0,0,0,0.15); z-index: 15; border: 2px solid;
}
.i1 { top: 10%; left: 50%; transform: translate(-50%, -50%); color: #3b82f6; border-color: #3b82f6;} 
.i2 { top: 38%; left: 88%; transform: translate(-50%, -50%); color: #ef4444; border-color: #ef4444;} 
.i3 { top: 82%; left: 74%; transform: translate(-50%, -50%); color: #4338ca; border-color: #4338ca;} 
.i4 { top: 82%; left: 26%; transform: translate(-50%, -50%); color: #f59e0b; border-color: #f59e0b;} 
.i5 { top: 38%; left: 12%; transform: translate(-50%, -50%); color: #10b981; border-color: #10b981;} 

.d-num {
    position: absolute; width: 36px; height: 36px; border-radius: 50%; color: white;
    display: flex; justify-content: center; align-items: center; font-size: 1.2rem; font-weight: 800;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2); z-index: 20; border: 3px solid white;
}
.n1 { top: 0%; left: 50%; transform: translate(-50%, -50%); background: #3b82f6; }
.n2 { top: 34.6%; left: 97.5%; transform: translate(-50%, -50%); background: #ef4444; }
.n3 { top: 90.4%; left: 79.3%; transform: translate(-50%, -50%); background: #4338ca; }
.n4 { top: 90.4%; left: 20.7%; transform: translate(-50%, -50%); background: #f59e0b; }
.n5 { top: 34.6%; left: 2.5%; transform: translate(-50%, -50%); background: #10b981; }

.d-arrow { position: absolute; color: white; font-size: 1.8rem; z-index: 12; font-weight: bold; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
.a1 { top: 17%; left: 72%; transform: translate(-50%, -50%) rotate(36deg); }
.a2 { top: 62%; left: 88%; transform: translate(-50%, -50%) rotate(108deg); }
.a3 { top: 88%; left: 50%; transform: translate(-50%, -50%) rotate(180deg); }
.a4 { top: 62%; left: 12%; transform: translate(-50%, -50%) rotate(252deg); }
.a5 { top: 17%; left: 28%; transform: translate(-50%, -50%) rotate(324deg); }

/* AJUSTE CLAVE: Tarjetas dinámicas que no se cortan */
.info-card { background: white; border-radius: 15px; padding: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.06); position: relative; transition: all 0.3s ease; border-top: 6px solid; height: auto !important; overflow: visible !important; word-wrap: break-word; }
.info-card:hover { transform: translateY(-5px); box-shadow: 0 20px 35px rgba(0,0,0,0.12); z-index: 20; }
.ic-1 { border-top-color: #3b82f6; grid-column: 1; grid-row: 1; }
.ic-2 { border-top-color: #ef4444; grid-column: 3; grid-row: 1; }
.ic-4 { border-top-color: #f59e0b; grid-column: 1; grid-row: 2; }
.ic-3 { border-top-color: #6366f1; grid-column: 3; grid-row: 2; }
.ic-5 { border-top-color: #10b981; grid-column: 1 / 4; grid-row: 3; margin-top: 15px;}

.card-header { display: flex; align-items: center; gap: 15px; margin-bottom: 10px; }
.card-num-box { width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 1.4rem; flex-shrink: 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.card-title { font-size: 1.15rem; font-weight: 800; margin: 0; line-height: 1.2; }
.card-details { margin-top: 15px; }
.card-details summary { font-weight: 700; cursor: pointer; padding: 12px 15px; border-radius: 8px; outline: none; list-style: none; transition: background 0.2s; display: flex; align-items: center; font-size: 0.9rem;}
.card-details summary::-webkit-details-marker { display: none; }
.card-details[open] summary { margin-bottom: 10px; }

/* AJUSTE CLAVE: Cuerpo de la tarjeta responsivo */
.card-body { padding: 15px; font-size: 0.85rem; line-height: 1.6; font-weight: 500; border-radius: 8px; border: 1px dashed; height: auto !important; overflow: visible !important; word-wrap: break-word;}

.bg-1 { background: #3b82f6; } .tc-1 { color: #1e40af; } .sum-1 { background: #eff6ff; color: #2563eb; } .bod-1 { background: #f8fafc; border-color: #bfdbfe; color: #334155; }
.bg-2 { background: #ef4444; } .tc-2 { color: #991b1b; } .sum-2 { background: #fef2f2; color: #dc2626; } .bod-2 { background: #fff5f5; border-color: #fecaca; color: #334155; }
.bg-3 { background: #4338ca; } .tc-3 { color: #312e81; } .sum-3 { background: #e0e7ff; color: #4338ca; } .bod-3 { background: #f8fafc; border-color: #c7d2fe; color: #334155; }
.bg-4 { background: #f59e0b; } .tc-4 { color: #92400e; } .sum-4 { background: #fffbeb; color: #d97706; } .bod-4 { background: #fefce8; border-color: #fde68a; color: #334155; }
.bg-5 { background: #10b981; } .tc-5 { color: #064e3b; } .sum-5 { background: #d1fae5; color: #059669; } .bod-5 { background: #f0fdf4; border-color: #a7f3d0; color: #334155; }

/* AJUSTE CLAVE: Responsividad móvil mejorada */
@media (max-width: 1024px) {
    .grid-infra { grid-template-columns: 1fr; grid-template-rows: auto; }
    .donut-wrapper { grid-column: 1; grid-row: 1; margin-bottom: 20px;}
    .ic-1 { grid-column: 1; grid-row: 2; }
    .ic-2 { grid-column: 1; grid-row: 3; }
    .ic-4 { grid-column: 1; grid-row: 4; }
    .ic-3 { grid-column: 1; grid-row: 5; }
    .ic-5 { grid-column: 1; grid-row: 6; }
    /* Permitir que la tarjeta se estire y gane espacio en celulares */
    .info-card { padding: 15px; height: auto !important; overflow: visible !important; }
    .card-body { height: auto !important; overflow: visible !important; }
}
</style>
'''
st.markdown(estilos, unsafe_allow_html=True)

# ==========================================
# DATOS BASE GLOBALES
# ==========================================
datos_hoja_ruta = pd.DataFrame({
    'Pilar': [
        '1. Seguridad Hídrica', '1. Seguridad Hídrica', '1. Seguridad Hídrica', '1. Seguridad Hídrica', '1. Seguridad Hídrica', '1. Seguridad Hídrica', '1. Seguridad Hídrica', '1. Seguridad Hídrica',
        '2. Suelo y Riesgo', '2. Suelo y Riesgo', '2. Suelo y Riesgo', '2. Suelo y Riesgo',
        '3. Plantas Beneficio', '3. Plantas Beneficio',
        '4. Aire y Ruido', '4. Aire y Ruido', '4. Aire y Ruido',
        '5. Biodiversidad', '5. Biodiversidad', '5. Biodiversidad', '5. Biodiversidad',
        '6. Ordenamiento Minero', '6. Ordenamiento Minero', '6. Ordenamiento Minero',
        '7. Info y Gobernanza', '7. Info y Gobernanza', '7. Info y Gobernanza'
    ],
    'Línea Estratégica': [
        '1. Inventario SIG hídrico', '2. Monitoreo molinos', '3. Red monitoreo cuenca', '4. Capacitación comunidad', '5. Control descargas ind.', '6. Recuperación cauces', '7. Tableros balance agua', '8. Capacitación personal',
        '9. Mapa riesgo operativo', '10. Obras escorrentía', '11. Estabilidad ladera', '12. Alternativas relaves',
        '13. Caracterizar plantas', '14. Ruta transición plantas',
        '15. Control de polvo', '16. Gestión ruido empresa', '17. Ruido minería trad.',
        '18. Monitoreo rondas', '19. Conectividad ecológica', '20. Recuperación progresiva', '21. Recup. formalización',
        '22. Matriz territorial', '23. Ruta transición', '24. Parque Minero',
        '25. SIG ambiental', '26. Mesa seguimiento', '27. Plan adaptación'
    ],
    'Problema Identificado': [
        'Falta línea base agua', 'Cambios en distribución', 'Falta monitoreo', 'Aportes lodos', 'Vertimientos ind.', 'Cauces colmatados', 'Baja eficiencia', 'Desconocimiento',
        'Inestabilidad', 'Escorrentía', 'Riesgo laderas', 'Manejo relaves',
        'Riesgo ambiental plantas', 'Plantas en riesgo',
        'Material particulado', 'Exposición ruido', 'Ruido minería',
        'Áreas degradadas', 'Fragmentación', 'Pasivos', 'Degradación formalización',
        'Falta info territorial', 'Desorden minero', 'Ausencia modelo integrado',
        'Datos dispersos', 'Falta seguimiento', 'Riesgo climático'
    ],
    'Prioridad': [
        '🔴 Crítica', '🔴 Crítica', '🔴 Crítica', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🔴 Crítica',
        '🔴 Crítica', '🟠 Alta', '🟠 Alta', '🟠 Alta',
        '🔴 Crítica', '🔴 Crítica',
        '🔴 Crítica', '🟠 Alta', '🟠 Alta',
        '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta',
        '🟠 Alta', '🟠 Alta', '🟠 Alta',
        '🟠 Alta', '🔴 Crítica', '🟠 Alta'
    ],
    'Responsable': [
        'Aris Mining', 'Alcaldía Municipal', 'Corpocaldas', 'Aris Mining', 'Aris Mining', 'Alcaldía Municipal', 'Aris Mining', 'Aris Mining',
        'Aris Mining', 'Aris Mining', 'ANM', 'Aris Mining',
        'Corpocaldas', 'ANM',
        'Aris Mining', 'Aris Mining', 'Alcaldía Municipal',
        'Aris Mining', 'Aris Mining', 'Aris Mining', 'Mineros Formalizados',
        'Alcaldía Municipal', 'ANM', 'MME',
        'Aris Mining', 'Aris Mining', 'Aris Mining'
    ],
    'Inicio': [
        '2026-06-01', '2026-06-01', '2026-06-01', '2026-06-01', '2026-06-01', '2026-12-01', '2026-12-01', '2026-06-01',
        '2026-06-01', '2026-06-01', '2026-06-01', '2026-06-01',
        '2026-06-01', '2026-12-01',
        '2026-06-01', '2026-06-01', '2026-06-01',
        '2026-12-01', '2026-12-01', '2026-12-01', '2029-06-01',
        '2026-06-01', '2027-06-01', '2028-06-01',
        '2026-06-01', '2026-06-01', '2027-06-01'
    ],
    'Fin': [
        '2026-12-01', '2026-12-01', '2026-12-01', '2027-12-01', '2027-12-01', '2029-06-01', '2028-06-01', '2026-12-01',
        '2026-12-01', '2028-06-01', '2028-06-01', '2028-06-01',
        '2027-03-01', '2029-06-01',
        '2026-12-01', '2027-12-01', '2027-12-01',
        '2029-06-01', '2029-06-01', '2030-06-01', '2031-06-01',
        '2027-06-01', '2029-06-01', '2031-06-01',
        '2027-06-01', '2026-09-01', '2029-06-01'
    ]
})

datos_conesa = pd.DataFrame({
    'Componente': ['Agua', 'Agua', 'Suelo', 'Suelo', 'Aire', 'Aire', 'Ruido', 'Ruido', 'Paisaje', 'Paisaje'],
    'Estado': ['Actual', 'Mitigado', 'Actual', 'Mitigado', 'Actual', 'Mitigado', 'Actual', 'Mitigado', 'Actual', 'Mitigado'],
    'IN': [10, 8, 10, 6, 8, 4, 8, 4, 11, 6], 'EX': [8, 6, 8, 6, 8, 4, 8, 4, 6, 6],
    'MO': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], 'PE': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    'RV': [4, 2, 4, 2, 4, 2, 4, 2, 4, 2], 'SI': [4, 4, 4, 2, 4, 2, 4, 2, 4, 2],
    'AC': [4, 4, 4, 4, 4, 2, 4, 2, 4, 2], 'EF': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    'PR': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], 'MC': [4, 2, 6, 2, 4, 2, 4, 2, 4, 2]
})
datos_conesa['Impacto Total'] = [-74, -70, -58, -36, -46, -22, -46, -22, -58, -39]

datos_prioridades = pd.DataFrame({
    'Orden': [1, 2, 3, 4, 5, 6, 7],
    'Tema_Corto': [
        'Minería, formalización y regulación', 
        'Desarrollo económico, empleo y formación', 
        'Gobernanza, institucionalidad y legalidad', 
        'Ambiente y agua', 
        'Seguridad, movilidad e infraestructura', 
        'Salud y bienestar social', 
        'Relacionamiento con Aris Mining'
    ],
    'Explicacion': [
        'Reglas claras y mayor acompañamiento en la formalización.', 
        'Más oportunidades de empleo, formación y apoyo a emprendimientos.', 
        'Mayor presencia del Estado, coordinación institucional y lucha contra la ilegalidad.', 
        'Control y monitoreo del agua, suelo y paisaje.', 
        'Mejores vías, movilidad segura y condiciones de infraestructura.', 
        'Mejor acceso a salud y mayor bienestar para las comunidades.', 
        'Más y mejor comunicación, mayor cercanía y presencia en el territorio.'
    ],
    'Proporción': [17.1, 17.1, 17.1, 14.3, 14.3, 11.4, 8.6],
    'Color': ['#176cb0', '#2ea952', '#f3b438', '#df3848', '#8a4ca9', '#24aebf', '#7f8185']
})
datos_prioridades['Temas Prioritarios'] = '<b>' + datos_prioridades['Tema_Corto'] + '</b><br><span style="font-size:11px; font-weight:normal;">' + datos_prioridades['Explicacion'] + '</span>'

datos_matriz = pd.DataFrame({
    'Iniciativa': [
        'Agua y ambiente', 'Convivencia minera', 'Población foránea', 'Comunicación de resultados',
        'Inclusión mujeres/jóvenes', 'Empleo y obras sociales', 'Formalización minera',
        'Cobertura inv. social', 'Vivienda e infraestructura', 'Seguridad minera', 'Transparencia y diálogo', 'Educación y capacidades'
    ],
    'Reconocimiento': [2.5, 4.5, 4.0, 2.0, 5.5, 8.5, 8.0, 2.5, 2.5, 8.5, 8.0, 6.0],
    'Necesidad': [8.5, 8.0, 6.5, 5.5, 7.0, 6.0, 8.5, 3.5, 1.8, 3.5, 2.0, 1.8],
    'Leyenda': ['67%', '71%', '70%', '56%', '74%', '62%', '67%', '49%', 'no se evidencia %', '66%', '63%', 'no se evidencia %'],
    'Cuadrante': [
        'Desafíos Críticos', 'Desafíos Críticos', 'Desafíos Críticos', 'Desafíos Críticos',
        'Oportunidades Estratégicas', 'Oportunidades Estratégicas', 'Oportunidades Estratégicas',
        'Seguimiento', 'Seguimiento', 'Activos para Consolidar', 'Activos para Consolidar', 'Activos para Consolidar'
    ],
    'Color': ['#e1364f', '#f3b438', '#e1364f', '#e1364f', '#f3b438', '#28a745', '#28a745', '#8e44ad', '#176cb0', '#00897b', '#00897b', '#00897b'],
    'Icono': ['💧', '🤝', '👥', '📢', '👩', '🏗️', '📜', '📊', '🏠', '⛑️', '💬', '🎓']
})

# --- NAVEGACIÓN LATERAL DINÁMICA ---
st.sidebar.markdown('''### 🧭 Menú de Navegación''')
seccion = st.sidebar.radio(
    "Selecciona un Nivel Estratégico:",
    ["🚀 Inicio: Relevancia de la Estrategia", "📊 0. Resumen Ejecutivo (Hoja de Ruta)", "🌿 1. Pilar Ambiental", "🤝 2. Pilar Social y Económico", "⚖️ 3. Pilar Gobernanza", "📡 4. Pilar Información", "♻️ 5. Pilar Sostenibilidad"]
)
st.sidebar.divider()

if seccion not in ["🌿 1. Pilar Ambiental", "🚀 Inicio: Relevancia de la Estrategia"]:
    st.sidebar.info('''💡 **Tip Gerencial:** Utiliza este panel para profundizar (*drill-down*) desde la vista general hacia los componentes específicos del diagnóstico territorial.''')

# =========================================================
# PÁGINA INICIO: RELEVANCIA ESTRATEGICA 
# =========================================================
if seccion == "🚀 Inicio: Relevancia de la Estrategia":
    html_hero = '''
<div class="macro-container">
<div class="header-info">
<h1>Estrategia de Sostenibilidad</h1>
<p>Hacia un territorio resiliente, integrado y con valor compartido</p>
</div>

<div class="grid-infra">

<div class="donut-wrapper">
<div class="donut-chart">
<div class="donut-inner">
<span style="font-size: 2.5rem; margin-bottom: 5px; display:block;">🏔️🏘️</span>
<b style="color: #1e3a8a; font-size: 1.2rem; line-height: 1.2;">Territorio<br>Sostenible</b>
<span style="font-size: 0.75rem; color: #64748b; margin-top: 8px; font-weight:600;">Diálogo, desarrollo<br>y bienestar</span>
</div>
<div class="d-icon i1">🗺️</div>
<div class="d-icon i2">⚙️</div>
<div class="d-icon i3">📊</div>
<div class="d-icon i4">🪙</div>
<div class="d-icon i5">🌱</div>
<div class="d-num n1">1</div>
<div class="d-num n2">2</div>
<div class="d-num n3">3</div>
<div class="d-num n4">4</div>
<div class="d-num n5">5</div>
<div class="d-arrow a1">➔</div>
<div class="d-arrow a2">➔</div>
<div class="d-arrow a3">➔</div>
<div class="d-arrow a4">➔</div>
<div class="d-arrow a5">➔</div>
</div>
</div>

<div class="info-card ic-1">
<div class="card-header"><div class="card-num-box bg-1">1</div><h3 class="card-title tc-1">Análisis y Contexto Territorial</h3></div>
<p style="font-size: 0.85rem; color:#64748b; margin-top:0;">Ambiental, Social, Económico (Datos y evidencia).</p>
<details class="card-details"><summary class="sum-1">▶ Ver componentes analizados</summary>
<div class="card-body bod-1">
<b>💧 Ambiental:</b> Agua, suelo y biodiversidad.<br><br>
<b>👥 Social:</b> Necesidades y expectativas locales.<br><br>
<b>💼 Económico:</b> Empleo y encadenamientos.<br><br>
<b>🗺️ Territorial:</b> Uso del suelo e infraestructura.
</div></details>
</div>

<div class="info-card ic-2">
<div class="card-header"><div class="card-num-box bg-2">2</div><h3 class="card-title tc-2">Enfoque de la Estrategia</h3></div>
<p style="font-size: 0.85rem; color:#64748b; margin-top:0;">Programas, Proyectos y Acciones con medición.</p>
<details class="card-details"><summary class="sum-2">▶ Ver ejes estratégicos</summary>
<div class="card-body bod-2">
<b>🤝 Generación de Confianza:</b> Relaciones sólidas.<br><br>
<b>🏗️ Estabilidad Territorial:</b> Condiciones a largo plazo.<br><br>
<b>🎯 Gestión:</b> Soluciones adaptadas al contexto.<br><br>
<b>💎 Sostenibilidad:</b> Base para el valor compartido.
</div></details>
</div>

<div class="info-card ic-3">
<div class="card-header"><div class="card-num-box bg-3">3</div><h3 class="card-title tc-3">Proyectos con Indicadores</h3></div>
<p style="font-size: 0.85rem; color:#64748b; margin-top:0;">Medición de impacto real en las comunidades.</p>
<details class="card-details"><summary class="sum-3">▶ Ver categorías de proyectos</summary>
<div class="card-body bod-3">
<b>🛣️ Infraestructura Vial:</b> Mejor conectividad.<br><br>
<b>🚰 Agua y Saneamiento:</b> Acceso a servicios básicos.<br><br>
<b>🏫 Infraestructura Social:</b> Espacios de bienestar.
</div></details>
</div>

<div class="info-card ic-4">
<div class="card-header"><div class="card-num-box bg-4">4</div><h3 class="card-title tc-4">Costos Evitados</h3></div>
<p style="font-size: 0.85rem; color:#64748b; margin-top:0;">Gestión proactiva para reducir riesgos operativos.</p>
<details class="card-details"><summary class="sum-4">▶ Ver riesgos mitigados</summary>
<div class="card-body bod-4">
<b>🚫 Reputacional:</b> Costo de Green Washing.<br><br>
<b>🚧 Interrupciones:</b> Paros y bloqueos.<br><br>
<b>⚠️ Incidentes:</b> Costos ambientales y sociales.<br><br>
<b>💰 Financiamiento:</b> Acceso a mercados de capital.<br><br>
<b>⚖️ Regulación:</b> Multas y sanciones.
</div></details>
</div>

<div class="info-card ic-5" style="display: flex; gap: 20px; align-items: center; flex-wrap: wrap;">
<div style="flex: 1; min-width: 250px;">
<div class="card-header"><div class="card-num-box bg-5">5</div><h3 class="card-title tc-5">Si se logra lo anterior se garantiza:</h3></div>
<p style="font-size: 0.95rem; color:#065f46; margin-top:10px; font-weight:600;">Una gestión social que genera valor compartido y fortalece el futuro de Marmato.</p>
</div>
<div style="flex: 2; display: flex; gap: 15px; flex-wrap: wrap;">
<div style="flex:1; min-width:120px; background: #ecfdf5; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #a7f3d0; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
<div style="font-size: 2rem;">🌿</div>
<div style="font-size: 0.85rem; font-weight: 700; color: #065f46; margin-top: 5px;">Sostenibilidad a largo plazo</div>
</div>
<div style="flex:1; min-width:120px; background: #ecfdf5; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #a7f3d0; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
<div style="font-size: 2rem;">📈</div>
<div style="font-size: 0.85rem; font-weight: 700; color: #065f46; margin-top: 5px;">Valor de mercado de la empresa</div>
</div>
<div style="flex:1; min-width:120px; background: #ecfdf5; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #a7f3d0; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
<div style="font-size: 2rem;">🏘️</div>
<div style="font-size: 0.85rem; font-weight: 700; color: #065f46; margin-top: 5px;">Mejoras en el territorio</div>
</div>
</div>
</div>

</div>
</div>
'''
    st.markdown(html_hero, unsafe_allow_html=True)

# =========================================================
# PÁGINA 0: RESUMEN EJECUTIVO 
# =========================================================
elif seccion == "📊 0. Resumen Ejecutivo (Hoja de Ruta)":
    st.markdown('''### 🎯 Panel de Control Gerencial: Ejecución de la Hoja de Ruta''')
    kpi_html = '''
<div class="kpi-container">
<div class="kpi-card"><div class="kpi-title">Líneas de Acción</div><div class="kpi-value">27</div><div class="kpi-delta delta-green">100% Planificadas</div></div>
<div class="kpi-card"><div class="kpi-title">Pilares Estratégicos</div><div class="kpi-value">7</div><div class="kpi-delta delta-green">Agrupación Temática</div></div>
<div class="kpi-card"><div class="kpi-title">Acciones Críticas</div><div class="kpi-value">9</div><div class="kpi-delta delta-red">Atención Inmediata</div></div>
<div class="kpi-card"><div class="kpi-title">Actores Clave</div><div class="kpi-value">6</div><div class="kpi-delta delta-orange">Entidades Directas</div></div>
</div>
'''
    st.markdown(kpi_html, unsafe_allow_html=True)
    st.divider()
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown('''#### 🏛️ Distribución por Pilar Estratégico (7 Ejes)''')
        fig_pilares = px.histogram(datos_hoja_ruta, y='Pilar', color='Prioridad', orientation='h', color_discrete_map={'🔴 Crítica': '#d62728', '🟠 Alta': '#ff7f0e'}, labels={'Pilar': ''})
        fig_pilares.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'}, margin=dict(t=10, b=10, l=10, r=10), height=380, plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Montserrat", color="black", size=13))
        st.plotly_chart(fig_pilares, use_container_width=True)
        
    with col_chart2:
        st.markdown('''#### 🤝 Responsabilidad de Ejecución (6 Actores)''')
        fig_pie = px.pie(datos_hoja_ruta, names='Responsable', hole=0.45, color_discrete_sequence=['#1E3A8A', '#10b981', '#f97316', '#ef4444', '#8b5cf6', '#06b6d4'])
        fig_pie.update_traces(textinfo='percent+label', textposition='inside', textfont_size=14, marker=dict(line=dict(color='#FFFFFF', width=2)))
        fig_pie.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=380, font=dict(family="Montserrat", color="black"))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    st.divider()
    st.markdown('''### 📋 Filtros de Exploración''')
    
    f_col1, f_col2, f_col3 = st.columns(3)
    filtro_pilar = f_col1.selectbox("Filtrar por Pilar:", ["Todos los Pilares"] + list(datos_hoja_ruta['Pilar'].unique()))
    filtro_prio = f_col2.selectbox("Filtrar por Prioridad:", ["Todas las Prioridades", "🔴 Crítica", "🟠 Alta"])
    filtro_resp = f_col3.selectbox("Filtrar por Actor Responsable:", ["Todos los Actores"] + list(datos_hoja_ruta['Responsable'].unique()))
    
    df_filtrado = datos_hoja_ruta.copy()
    if filtro_pilar != "Todos los Pilares": df_filtrado = df_filtrado[df_filtrado['Pilar'] == filtro_pilar]
    if filtro_prio != "Todas las Prioridades": df_filtrado = df_filtrado[df_filtrado['Prioridad'] == filtro_prio]
    if filtro_resp != "Todos los Actores": df_filtrado = df_filtrado[df_filtrado['Responsable'] == filtro_resp]
        
    tab_tabla, tab_gantt = st.tabs(["📋 Detalles e Iniciativas", "📅 Cronograma Estratégico (Gantt)"])
    
    with tab_tabla:
        df_visual = df_filtrado[['Pilar', 'Línea Estratégica', 'Prioridad', 'Responsable']].style.set_properties(**{
            'color': '#111827', 'font-weight': '600', 'font-size': '15px', 'background-color': '#f8fafc', 'border-color': '#e5e7eb'
        })
        st.dataframe(df_visual, use_container_width=True, hide_index=True)
        
        with st.expander("👁️ Ver diagnóstico técnico que origina estas acciones"):
            st.markdown('''**Justificación Técnica / Problema Base:**''')
            df_diag_visual = df_filtrado[['Línea Estratégica', 'Problema Identificado']].style.set_properties(**{
                'color': '#1F2937', 'font-weight': '500', 'font-size': '14px', 'background-color': '#f3f4f6'
            })
            st.dataframe(df_diag_visual, use_container_width=True, hide_index=True)
            
    with tab_gantt:
        if not df_filtrado.empty:
            df_filtrado_gantt = df_filtrado.copy()
            df_filtrado_gantt['Orden_Numérico'] = df_filtrado_gantt['Línea Estratégica'].str.extract(r'^(\d+)').astype(int)
            df_filtrado_gantt['Inicio'] = pd.to_datetime(df_filtrado_gantt['Inicio'])
            df_filtrado_gantt['Fin'] = pd.to_datetime(df_filtrado_gantt['Fin'])
            df_filtrado_gantt['Meses'] = ((df_filtrado_gantt['Fin'] - df_filtrado_gantt['Inicio']).dt.days / 30).astype(int)
            df_filtrado_gantt['Etiqueta'] = "+ " + df_filtrado_gantt['Meses'].astype(str) + " Meses"
            
            df_filtrado_gantt = df_filtrado_gantt.sort_values(by=["Inicio", "Orden_Numérico"], ascending=[True, True])
            
            fig_gantt = px.timeline(
                df_filtrado_gantt, 
                x_start="Inicio", 
                x_end="Fin", 
                y="Línea Estratégica", 
                color="Prioridad", 
                text="Etiqueta",
                color_discrete_map={'🔴 Crítica': '#d62728', '🟠 Alta': '#ff7f0e'}
            )
            fig_gantt.update_yaxes(autorange="reversed") 
            fig_gantt.update_traces(textposition='outside')
            fig_gantt.update_layout(
                height=800, 
                plot_bgcolor='rgba(0,0,0,0)', 
                font=dict(family="Montserrat", color="black"),
                xaxis_title="Proyección de Tiempo",
                yaxis_title="",
                legend_title="Prioridad"
            )
            fig_gantt.update_xaxes(showgrid=True, gridcolor='#e5e7eb', dtick="M12")
            st.plotly_chart(fig_gantt, use_container_width=True)
        else:
            st.warning('''No hay iniciativas que coincidan con los filtros seleccionados.''')

# =========================================================
# PILAR 1: AMBIENTAL 
# =========================================================
elif seccion == "🌿 1. Pilar Ambiental":
    st.header('''🌿 Pilar 1: Gestión Ambiental y del Territorio''')
    st.markdown('''Enfoque en la conectividad ecológica, gestión del recurso hídrico y estabilización de taludes.''')
    
    pestaña_p1 = st.radio("Selecciona una vista:", ["📉 Impacto Global", "🔍 Desglose por Componente", "🌲 Inteligencia Territorial y Biodiversidad"], horizontal=True, label_visibility="collapsed")
    
    if pestaña_p1 in ["📉 Impacto Global", "🔍 Desglose por Componente"]:
        st.sidebar.markdown('''
<div style="background-color: #e0f2fe; padding: 15px; border-radius: 8px; border: 1px solid #bae6fd; font-size: 0.9em; margin-top: 15px;">
<p style="margin-bottom: 10px; color: #0369a1; font-weight: bold;">💡 Diccionario CONESA:</p>
<p style="margin-bottom: 6px;"><b>IN:</b> Intensidad</p>
<p style="margin-bottom: 6px;"><b>EX:</b> Extensión</p>
<p style="margin-bottom: 6px;"><b>MO:</b> Momento</p>
<p style="margin-bottom: 6px;"><b>PE:</b> Persistencia</p>
<p style="margin-bottom: 6px;"><b>RV:</b> Reversibilidad</p>
<p style="margin-bottom: 6px;"><b>SI:</b> Sinergia</p>
<p style="margin-bottom: 6px;"><b>AC:</b> Acumulación</p>
<p style="margin-bottom: 6px;"><b>EF:</b> Efecto</p>
<p style="margin-bottom: 6px;"><b>PR:</b> Periodicidad</p>
<p style="margin-bottom: 0px;"><b>MC:</b> Recuperabilidad</p>
</div>
''', unsafe_allow_html=True)

    st.divider()

    colores_conesa = {
        'Agua': {'Actual': '#1f77b4', 'Mitigado': '#aec7e8'},
        'Suelo': {'Actual': '#8c564b', 'Mitigado': '#c49c94'},
        'Aire': {'Actual': '#17becf', 'Mitigado': '#9edae5'},
        'Ruido': {'Actual': '#9467bd', 'Mitigado': '#c5b0d5'},
        'Paisaje': {'Actual': '#2ca02c', 'Mitigado': '#98df8a'}
    }

    if pestaña_p1 == "📉 Impacto Global":
        st.markdown('''### Evaluación de Impacto CONESA (Actual vs. Mitigado)''')
        
        datos_conesa['Color'] = datos_conesa.apply(lambda row: colores_conesa[row['Componente']][row['Estado']], axis=1)
        
        fig_conesa1 = go.Figure()
        for estado in ['Actual', 'Mitigado']:
            df_est = datos_conesa[datos_conesa['Estado'] == estado]
            fig_conesa1.add_trace(go.Bar(
                y=df_est['Componente'],
                x=df_est['Impacto Total'],
                name=estado,
                orientation='h',
                marker_color=df_est['Color'],
                text=estado,
                textposition='inside',
                insidetextanchor='start'
            ))
            
        fig_conesa1.update_layout(
            barmode='group', 
            height=400, 
            plot_bgcolor='white', 
            xaxis_title="Impacto Total", 
            yaxis_title="Componente", 
            margin=dict(l=0, r=0, t=30, b=0), 
            showlegend=False
        )
        st.plotly_chart(fig_conesa1, use_container_width=True)

        st.markdown('''<br>''', unsafe_allow_html=True)
        st.markdown('''### 🛡️ Potencial de Mitigación por Componente''')
        
        html_potencial = '''
<div style="display: flex; gap: 15px; flex-wrap: wrap;">
<details class="kpi-btn">
<summary>
<div class="kpi-btn-title">Agua</div>
<div class="kpi-btn-value">-74</div>
<div class="kpi-btn-delta">+4 pts recup.</div><br>
<div class="click-hint-kpi">▶ Ver medida</div>
</summary>
<div class="expanded-content-kpi">
<b>Medida de Manejo:</b> Construcción de plantas de tratamiento de vertimientos (PTAR) e inventario hídrico en quebradas críticas.
</div>
</details>

<details class="kpi-btn">
<summary>
<div class="kpi-btn-title">Aire</div>
<div class="kpi-btn-value">-46</div>
<div class="kpi-btn-delta">+24 pts recup.</div><br>
<div class="click-hint-kpi">▶ Ver medida</div>
</summary>
<div class="expanded-content-kpi">
<b>Medida de Manejo:</b> Humectación de vías operativas, pavimentación de tramos críticos y cerramientos anti-polvo.
</div>
</details>

<details class="kpi-btn">
<summary>
<div class="kpi-btn-title">Paisaje</div>
<div class="kpi-btn-value">-58</div>
<div class="kpi-btn-delta">+19 pts recup.</div><br>
<div class="click-hint-kpi">▶ Ver medida</div>
</summary>
<div class="expanded-content-kpi">
<b>Medida de Manejo:</b> Conformación de taludes, revegetación progresiva y barreras forestales perimetrales.
</div>
</details>

<details class="kpi-btn">
<summary>
<div class="kpi-btn-title">Ruido</div>
<div class="kpi-btn-value">-46</div>
<div class="kpi-btn-delta">+24 pts recup.</div><br>
<div class="click-hint-kpi">▶ Ver medida</div>
</summary>
<div class="expanded-content-kpi">
<b>Medida de Manejo:</b> Aislamiento acústico en plantas de beneficio, control de horarios de transporte y mantenimiento de maquinaria.
</div>
</details>

<details class="kpi-btn">
<summary>
<div class="kpi-btn-title">Suelo</div>
<div class="kpi-btn-value">-58</div>
<div class="kpi-btn-delta">+22 pts recup.</div><br>
<div class="click-hint-kpi">▶ Ver medida</div>
</summary>
<div class="expanded-content-kpi">
<b>Medida de Manejo:</b> Control de escorrentía, estabilización de laderas y manejo adecuado de estériles y relaves.
</div>
</details>
</div>
'''
        st.markdown(html_potencial, unsafe_allow_html=True)

    elif pestaña_p1 == "🔍 Desglose por Componente":
        comp_sel = st.selectbox("Elige un Componente:", ["Agua", "Suelo", "Aire", "Ruido", "Paisaje"])
        df_melted = datos_conesa.melt(id_vars=['Componente', 'Estado'], value_vars=['IN', 'EX', 'MO', 'PE', 'RV', 'SI', 'AC', 'EF', 'PR', 'MC'], var_name='Variable', value_name='Puntaje')
        df_comp = df_melted[df_melted['Componente'] == comp_sel]

        fig_conesa2 = px.bar(df_comp, x='Puntaje', y='Variable', color='Estado', barmode='group', orientation='h',
                             color_discrete_map=colores_conesa[comp_sel])
        fig_conesa2.update_layout(height=450, plot_bgcolor='white', xaxis_title="Puntaje", yaxis_title="Variable", margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_conesa2, use_container_width=True)

        with st.expander("📊 Ver Matriz Cuantitativa Completa"):
            st.dataframe(datos_conesa, use_container_width=True)

    elif pestaña_p1 == "🌲 Inteligencia Territorial y Biodiversidad":
        html_kpis_interactivos = '''
<div class="kpi-container" style="padding-top: 15px;">
<details class="kpi-btn">
<summary>
<div class="kpi-btn-title">🌳 Bosque Recuperado<br><span style="font-size: 0.8em; font-weight: 500; color: #6b7280;">(2018-2026)</span></div>
<div class="kpi-btn-value">+201.5 ha</div>
<div class="kpi-btn-delta">Vs +18.6 ha (2018-2021)</div><br>
<div class="click-hint-kpi">Picar para ver análisis ▼</div>
</summary>
<div class="expanded-content-kpi">Fuerte proceso de sucesión ecológica positiva. La vegetación secundaria se ha consolidado en bosque maduro estructural.</div>
</details>
<details class="kpi-btn">
<summary>
<div class="kpi-btn-title">⛏ Exp. Superficie Minera<br><span style="font-size: 0.8em; font-weight: 500; color: #6b7280;">(2018-2026)</span></div>
<div class="kpi-btn-value">-2.04 ha</div>
<div class="kpi-btn-delta">Vs +8.00 ha (2018-2021)</div><br>
<div class="click-hint-kpi">Picar para ver análisis ▼</div>
</summary>
<div class="expanded-content-kpi">Reducción neta del crecimiento de áreas mineras degradadas, marcando un freno a la expansión desordenada del pasado.</div>
</details>
<details class="kpi-btn">
<summary>
<div class="kpi-btn-title">🏭 Exp. Urbano-Industrial<br><span style="font-size: 0.8em; font-weight: 500; color: #6b7280;">(2018-2026)</span></div>
<div class="kpi-btn-value">-0.29 ha</div>
<div class="kpi-btn-delta">Vs +22.65 ha (2018-2021)</div><br>
<div class="click-hint-kpi">Picar para ver análisis ▼</div>
</summary>
<div class="expanded-content-kpi">Estabilización del crecimiento urbano y de infraestructura tras un periodo de alta alteración de las coberturas.</div>
</details>
</div>
'''
        st.markdown(html_kpis_interactivos, unsafe_allow_html=True)
        st.divider()
        
        st.markdown('''#### 🔄 Dinámica de Transición de Coberturas (Diagrama de Flujo)''')
        
        link_colors = [
            'rgba(0,109,44,0.4)', 'rgba(116,196,118,0.4)', 'rgba(116,196,118,0.4)', 'rgba(254,196,79,0.4)', 'rgba(161,217,155,0.65)', 
            'rgba(161,217,155,0.65)', 'rgba(161,217,155,0.65)', 'rgba(161,217,155,0.65)', 'rgba(117,107,177,0.4)', 'rgba(150,150,150,0.4)', 
            'rgba(206,18,86,0.4)', 'rgba(107,174,214,0.4)', 'rgba(0,109,44,0.4)', 'rgba(116,196,118,0.4)', 'rgba(116,196,118,0.6)', 
            'rgba(254,196,79,0.4)', 'rgba(161,217,155,0.65)', 'rgba(117,107,177,0.4)', 'rgba(150,150,150,0.4)', 'rgba(206,18,86,0.4)', 'rgba(107,174,214,0.4)'
        ]
        c_bosque, c_veg, c_cultivos, c_pastos, c_suelos, c_urbano, c_mineria, c_agua = '#006d2c', '#74c476', '#fec44f', '#e5f5e0', '#756bb1', '#969696', '#ce1256', '#6baed6'
        labels_sankey = ["🌲 Bosque", "🌱 Veg. Sec.", "🌾 Cultivos", "🌿 Pastos", "🪨 Suelos D.", "🏭 Urbano", "⛏️ Minería", "💧 Agua"] * 3 
        colors_nodes_sankey = [c_bosque, c_veg, c_cultivos, c_pastos, c_suelos, c_urbano, c_mineria, c_agua] * 3
        fuentes = [0, 1, 1, 2, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 9, 10, 11, 12, 13, 14, 15]
        destinos = [8, 9, 8, 10, 11, 12, 13, 14, 12, 13, 14, 15, 16, 17, 16, 18, 19, 20, 21, 22, 23]
        valores_sankey = [220, 461.36, 18.64, 19.5, 298.8, 13.24, 22.65, 8.0, 16, 42, 16, 2, 238.64, 263.96, 205.22, 7.2, 311.1, 29.24, 64.65, 24, 2]

        fig_sankey = go.Figure(data=[go.Sankey(
            arrangement="snap",
            node=dict(
                pad=18, thickness=30, line=dict(color="white", width=2), label=labels_sankey, color=colors_nodes_sankey,
                hovertemplate='<b>%{label}</b><br>Total: %{value} ha<extra></extra>'
            ),
            link=dict(
                source=fuentes, target=destinos, value=valores_sankey, color=link_colors,
                hovertemplate='<b>Origen:</b> %{source.label}<br><b>Destino:</b> %{target.label}<br><b>Transición:</b> %{value} ha<extra></extra>'
            )
        )])
        
        fig_sankey.update_layout(height=450, font=dict(family="Montserrat", size=12, color="#1f2937"), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=40, b=20, l=10, r=10))
        fig_sankey.add_annotation(x=0.02, y=1.08, text="<b>AÑO 2018</b>", showarrow=False, xref="paper", yref="paper", font=dict(size=14))
        fig_sankey.add_annotation(x=0.5, y=1.08, text="<b>AÑO 2021</b>", showarrow=False, xref="paper", yref="paper", font=dict(size=14))
        fig_sankey.add_annotation(x=0.98, y=1.08, text="<b>AÑO 2026</b>", showarrow=False, xref="paper", yref="paper", font=dict(size=14))
        st.plotly_chart(fig_sankey, use_container_width=True)
        
        html_hallazgos = '''
<div style="display: flex; gap: 15px; flex-wrap: wrap;">
<details style="flex:1; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); cursor: pointer; transition: all 0.2s;">
<summary style="padding: 12px 15px; outline: none; list-style: none; font-weight: 600; color: #475569; font-size: 0.9rem; display: flex; align-items: center; border-bottom: 1px solid #f1f5f9;">
<span style="margin-right: 10px; font-size: 1.1rem; color: #f59e0b;">💡</span> ¿Qué significa este hallazgo (Efecto Título)?
</summary>
<div style="padding: 15px; font-size: 0.9rem; color: #1e3a8a; line-height: 1.5; background: #eff6ff; border-radius: 0 0 8px 8px; margin: 10px;">
La llegada de la compañía en 2021 coincide con un cambio de tendencia drástico: el bosque (línea verde) acelera su crecimiento exponencialmente, mientras que la expansión desordenada de superficies mineras e industriales se frena y estabiliza.
</div>
</details>

<details style="flex:1; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); cursor: pointer; transition: all 0.2s;">
<summary style="padding: 12px 15px; outline: none; list-style: none; font-weight: 600; color: #475569; font-size: 0.9rem; display: flex; align-items: center; border-bottom: 1px solid #f1f5f9;">
<span style="margin-right: 10px; font-size: 1.1rem; color: #f59e0b;">💡</span> ¿Qué significa este hallazgo (Sucesión Ecológica)?
</summary>
<div style="padding: 15px; font-size: 0.9rem; color: #1e3a8a; line-height: 1.5; background: #eff6ff; border-radius: 0 0 8px 8px; margin: 10px;">
La gran barra roja refleja la transformación de la vegetación secundaria (-205 ha), que fue reemplazada casi simétricamente por bosque maduro (barra verde, +201 ha), evidenciando un proceso natural de sucesión ecológica positiva en el título.
</div>
</details>
</div>
'''
        st.markdown(html_hallazgos, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown('''#### 🧩 Matriz Dinámica y Espacial de Restauración Inteligente''')
        
        corredor_sel = st.selectbox(
            "Selecciona un Corredor Priorizado para ver su análisis espacial y estratégico:", 
            options=["Conexión 1 ↔ 5 (Sector San Juan)", "Conexión 2 ↔ 4 (Echandía - Llano Grande)"],
            index=None,
            placeholder="Pica aquí para elegir entre los 2 corredores priorizados..."
        )
        
        if corredor_sel is None:
            st.info('''👆 Por favor, despliega el menú de arriba y selecciona uno de los dos corredores ecológicos para visualizar su perfil de inversión y mapa satelital.''')
        else:
            col_datos, col_mapa = st.columns([1, 1.4])
            if corredor_sel == "Conexión 1 ↔ 5 (Sector San Juan)":
                perfil, esfuerzo, impacto, accion = "Alta Eficiencia Costo-Beneficio", "Bajo / Medio", "Conecta fragmentos rápidamente", "Pasos de fauna rápidos"
                lats_poly, lons_poly = [5.460, 5.455, 5.455, 5.460, 5.460], [-75.6095, -75.6115, -75.6125, -75.6105, -75.6095]
                centro = {"lat": 5.4575, "lon": -75.6110}
                color_hex = "#3b82f6"
            else:
                perfil, esfuerzo, impacto, accion = "Intervención Estructural Profunda", "Alto (Largo Plazo)", "Aumenta conectividad global 15%", "Restauración forestal pesada"
                lats_poly, lons_poly = [5.478, 5.470, 5.470, 5.478, 5.478], [-75.5845, -75.5875, -75.5885, -75.5855, -75.5845]
                centro = {"lat": 5.4740, "lon": -75.5865}
                color_hex = "#f97316"
            
            with col_datos:
                html_corredores = f'''
<div style="display: flex; flex-direction: column; gap: 12px;">
<div style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px; border-left: 5px solid {color_hex};">
<div style="font-size: 0.85em; color: #6b7280; font-weight: 600;">📊 Perfil de Inversión</div>
<div style="font-size: 1.15em; font-weight: 700;">{perfil}</div>
</div>
<div style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px; border-left: 5px solid #ef4444;">
<div style="font-size: 0.85em; color: #6b7280; font-weight: 600;">⏱️ Nivel de Esfuerzo</div>
<div style="font-size: 1.15em; font-weight: 700;">{esfuerzo}</div>
</div>
<div style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px; border-left: 5px solid #10b981;">
<div style="font-size: 0.85em; color: #6b7280; font-weight: 600;">🌿 Impacto Ecológico</div>
<div style="font-size: 1.15em; font-weight: 700;">{impacto}</div>
</div>
</div>
'''
                st.markdown(html_corredores, unsafe_allow_html=True)

            with col_mapa:
                coords = [[lon, lat] for lon, lat in zip(lons_poly, lats_poly)]
                df_poly = pd.DataFrame({"coordinates": [coords]})
                
                if color_hex == "#3b82f6":
                    fill_color = [59, 130, 246, 140]
                    line_color = [59, 130, 246, 255]
                else:
                    fill_color = [249, 115, 22, 140]
                    line_color = [249, 115, 22, 255]

                # 1. Capa Satelital Base
                layer_satelite = pdk.Layer(
                    "TileLayer",
                    data="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                )
                
                # 2. Capa de Etiquetas y Vías (El efecto híbrido)
                layer_etiquetas = pdk.Layer(
                    "TileLayer",
                    data="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
                )

                # 3. Capa del Polígono (El corredor ecológico)
                layer_poly = pdk.Layer(
                    "PolygonLayer",
                    data=df_poly,
                    get_polygon="coordinates",
                    get_fill_color=fill_color,
                    get_line_color=line_color,
                    line_width_min_pixels=3,
                    extruded=False
                )

                view_state = pdk.ViewState(
                    latitude=centro["lat"],
                    longitude=centro["lon"],
                    zoom=14.5,
                    pitch=20
                )

                # Se cargan las 3 capas en orden: Satélite -> Etiquetas -> Polígono
                st.pydeck_chart(pdk.Deck(
                    layers=[layer_satelite, layer_etiquetas, layer_poly],
                    initial_view_state=view_state,
                    map_style=None
                ), use_container_width=True)

# =========================================================
# PILAR 2: SOCIAL Y ECONÓMICO
# =========================================================
elif seccion == "🤝 2. Pilar Social y Económico":
    st.header('''🤝 Pilar 2: Relacionamiento, Confianza y Economía''')
    
    tab_actores, tab_balanza, tab_prioridades = st.
