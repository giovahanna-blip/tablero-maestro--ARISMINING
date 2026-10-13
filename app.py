import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
details.kpi-btn { flex: 1; min-width: 220px; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px 15px; text-align: center; transition: all 0.2s ease-in-out; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
details.kpi-btn:hover { transform: translateY(-4px); box-shadow: 0 10px 15px rgba(0,0,0,0.1); border-color: #10b981; }
details.kpi-btn summary { list-style: none; outline: none; }
details.kpi-btn summary::-webkit-details-marker { display: none; }
.kpi-btn-title { font-size: 1.05em; color: #374151; margin-bottom: 5px; font-weight: 700; line-height: 1.3;}
.kpi-btn-value { font-size: 2.8em; font-weight: 800; color: #1E3A8A; margin: 10px 0; line-height: 1.1; }
.kpi-btn-delta { font-size: 0.85em; padding: 6px 14px; border-radius: 20px; display: inline-block; font-weight: 700; border: 1px solid #bbf7d0; background-color: #d1fae5; color: #065f46;}
.click-hint-kpi { font-size: 0.7rem; color: #6b7280; margin-top: 15px; font-weight: 600; background: #f3f4f6; border-radius: 10px; padding: 4px 10px; display: inline-block;}
details.kpi-btn[open] .click-hint-kpi { display: none; }
.expanded-content-kpi { margin-top: 15px; padding-top: 12px; border-top: 1px dashed #d1d5db; font-size: 0.85rem; color: #4b5563; font-weight: 500; line-height: 1.4; }

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

/* Contenedores de botones Pilar 5 */
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

/* Cuadrícula interna */
.grid-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; width: 100%;}
.grid-item { background: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; border-top: 4px solid; }

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
    /* Degradado cónico simulando gráfico de anillos con separaciones transparentes */
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
/* Íconos Flotantes sobre el Anillo */
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

/* Números Flotantes en el Borde Exterior */
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

/* Flechas del Ciclo */
.d-arrow { position: absolute; color: white; font-size: 1.8rem; z-index: 12; font-weight: bold; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
.a1 { top: 17%; left: 72%; transform: translate(-50%, -50%) rotate(36deg); }
.a2 { top: 62%; left: 88%; transform: translate(-50%, -50%) rotate(108deg); }
.a3 { top: 88%; left: 50%; transform: translate(-50%, -50%) rotate(180deg); }
.a4 { top: 62%; left: 12%; transform: translate(-50%, -50%) rotate(252deg); }
.a5 { top: 17%; left: 28%; transform: translate(-50%, -50%) rotate(324deg); }

/* Tarjetas Flotantes Laterales */
.info-card { background: white; border-radius: 15px; padding: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.06); position: relative; transition: all 0.3s ease; border-top: 6px solid; }
.info-card:hover { transform: translateY(-5px); box-shadow: 0 20px 35px rgba(0,0,0,0.12); z-index: 20; }
.ic-1 { border-top-color: #3b82f6; grid-column: 1; grid-row: 1; }
.ic-2 { border-top-color: #ef4444; grid-column: 3; grid-row: 1; }
.ic-4 { border-top-color: #f59e0b; grid-column: 1; grid-row: 2; }
.ic-3 { border-top-color: #6366f1; grid-column: 3; grid-row: 2; }
.ic-5 { border-top-color: #10b981; grid-column: 1 / 4; grid-row: 3; margin-top: 15px;}

/* Interior Tarjetas */
.card-header { display: flex; align-items: center; gap: 15px; margin-bottom: 10px; }
.card-num-box { width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 1.4rem; flex-shrink: 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.card-title { font-size: 1.15rem; font-weight: 800; margin: 0; line-height: 1.2; }
.card-details { margin-top: 15px; }
.card-details summary { font-weight: 700; cursor: pointer; padding: 12px 15px; border-radius: 8px; outline: none; list-style: none; transition: background 0.2s; display: flex; align-items: center; font-size: 0.9rem;}
.card-details summary::-webkit-details-marker { display: none; }
.card-details[open] summary { margin-bottom: 10px; }
.card-body { padding: 15px; font-size: 0.85rem; line-height: 1.6; font-weight: 500; border-radius: 8px; border: 1px dashed; }

.bg-1 { background: #3b82f6; } .tc-1 { color: #1e40af; } .sum-1 { background: #eff6ff; color: #2563eb; } .bod-1 { background: #f8fafc; border-color: #bfdbfe; color: #334155; }
.bg-2 { background: #ef4444; } .tc-2 { color: #991b1b; } .sum-2 { background: #fef2f2; color: #dc2626; } .bod-2 { background: #fff5f5; border-color: #fecaca; color: #334155; }
.bg-3 { background: #4338ca; } .tc-3 { color: #312e81; } .sum-3 { background: #e0e7ff; color: #4338ca; } .bod-3 { background: #f8fafc; border-color: #c7d2fe; color: #334155; }
.bg-4 { background: #f59e0b; } .tc-4 { color: #92400e; } .sum-4 { background: #fffbeb; color: #d97706; } .bod-4 { background: #fefce8; border-color: #fde68a; color: #334155; }
.bg-5 { background: #10b981; } .tc-5 { color: #064e3b; } .sum-5 { background: #d1fae5; color: #059669; } .bod-5 { background: #f0fdf4; border-color: #a7f3d0; color: #334155; }

/* Responsividad general */
@media (max-width: 1024px) {
    .grid-infra { grid-template-columns: 1fr; grid-template-rows: auto; }
    .donut-wrapper { grid-column: 1; grid-row: 1; margin-bottom: 20px;}
    .ic-1 { grid-column: 1; grid-row: 2; }
    .ic-2 { grid-column: 1; grid-row: 3; }
    .ic-4 { grid-column: 1; grid-row: 4; }
    .ic-3 { grid-column: 1; grid-row: 5; }
    .ic-5 { grid-column: 1; grid-row: 6; }
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

<!-- NÚCLEO CENTRAL CIRCULAR -->
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

<!-- TARJETAS -->
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
            <div style="flex:1; min-width: 140px; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; text-align: center; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <div style="font-size: 0.95rem; color: #4b5563; font-weight: 600; margin-bottom: 10px;">Agua</div>
                <div style="font-size: 2rem; color: #1e3a8a; font-weight: 800; margin-bottom: 15px;">-74</div>
                <div style="background: #d1fae5; color: #065f46; font-size: 0.85rem; font-weight: 700; padding: 5px 15px; border-radius: 20px; display: inline-block; margin-bottom: 15px;">+4 pts recup.</div><br>
                <div style="font-size: 0.8rem; color: #6b7280; font-weight:600; cursor: pointer;">▶ <span style="color:#ef4444;">❓</span> Ver medida</div>
            </div>
            <div style="flex:1; min-width: 140px; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; text-align: center; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <div style="font-size: 0.95rem; color: #4b5563; font-weight: 600; margin-bottom: 10px;">Aire</div>
                <div style="font-size: 2rem; color: #1e3a8a; font-weight: 800; margin-bottom: 15px;">-46</div>
                <div style="background: #d1fae5; color: #065f46; font-size: 0.85rem; font-weight: 700; padding: 5px 15px; border-radius: 20px; display: inline-block; margin-bottom: 15px;">+24 pts recup.</div><br>
                <div style="font-size: 0.8rem; color: #6b7280; font-weight:600; cursor: pointer;">▶ <span style="color:#ef4444;">❓</span> Ver medida</div>
            </div>
            <div style="flex:1; min-width: 140px; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; text-align: center; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <div style="font-size: 0.95rem; color: #4b5563; font-weight: 600; margin-bottom: 10px;">Paisaje</div>
                <div style="font-size: 2rem; color: #1e3a8a; font-weight: 800; margin-bottom: 15px;">-58</div>
                <div style="background: #d1fae5; color: #065f46; font-size: 0.85rem; font-weight: 700; padding: 5px 15px; border-radius: 20px; display: inline-block; margin-bottom: 15px;">+19 pts recup.</div><br>
                <div style="font-size: 0.8rem; color: #6b7280; font-weight:600; cursor: pointer;">▶ <span style="color:#ef4444;">❓</span> Ver medida</div>
            </div>
            <div style="flex:1; min-width: 140px; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; text-align: center; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <div style="font-size: 0.95rem; color: #4b5563; font-weight: 600; margin-bottom: 10px;">Ruido</div>
                <div style="font-size: 2rem; color: #1e3a8a; font-weight: 800; margin-bottom: 15px;">-46</div>
                <div style="background: #d1fae5; color: #065f46; font-size: 0.85rem; font-weight: 700; padding: 5px 15px; border-radius: 20px; display: inline-block; margin-bottom: 15px;">+24 pts recup.</div><br>
                <div style="font-size: 0.8rem; color: #6b7280; font-weight:600; cursor: pointer;">▶ <span style="color:#ef4444;">❓</span> Ver medida</div>
            </div>
            <div style="flex:1; min-width: 140px; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; text-align: center; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <div style="font-size: 0.95rem; color: #4b5563; font-weight: 600; margin-bottom: 10px;">Suelo</div>
                <div style="font-size: 2rem; color: #1e3a8a; font-weight: 800; margin-bottom: 15px;">-58</div>
                <div style="background: #d1fae5; color: #065f46; font-size: 0.85rem; font-weight: 700; padding: 5px 15px; border-radius: 20px; display: inline-block; margin-bottom: 15px;">+22 pts recup.</div><br>
                <div style="font-size: 0.8rem; color: #6b7280; font-weight:600; cursor: pointer;">▶ <span style="color:#ef4444;">❓</span> Ver medida</div>
            </div>
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
                lats_nodos, lons_nodos = [5.460, 5.455], [-75.610, -75.612]
                lats_poly, lons_poly = [5.460, 5.455, 5.455, 5.460, 5.460], [-75.6095, -75.6115, -75.6125, -75.6105, -75.6095]
                centro, color_hex, color_rgba, nombres = {"lat": 5.4575, "lon": -75.6110}, "#3b82f6", "rgba(59, 130, 246, 0.5)", ["Núcleo Boscoso 1", "Núcleo Boscoso 5"]
            else:
                perfil, esfuerzo, impacto, accion = "Intervención Estructural Profunda", "Alto (Largo Plazo)", "Aumenta conectividad global 15%", "Restauración forestal pesada"
                lats_nodos, lons_nodos = [5.478, 5.470], [-75.585, -75.588]
                lats_poly, lons_poly = [5.478, 5.470, 5.470, 5.478, 5.478], [-75.5845, -75.5875, -75.5885, -75.5855, -75.5845]
                centro, color_hex, color_rgba, nombres = {"lat": 5.4740, "lon": -75.5865}, "#f97316", "rgba(249, 115, 22, 0.5)", ["Núcleo Boscoso 2", "Núcleo Boscoso 4"]
            
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
                fig_mapa = go.Figure()
                fig_mapa.add_trace(go.Scattermapbox(mode="lines", lon=lons_poly, lat=lats_poly, fill="toself", fillcolor=color_rgba, line=dict(width=1, color=color_hex), hoverinfo="none"))
                fig_mapa.add_trace(go.Scattermapbox(mode="markers", lon=lons_nodos, lat=lats_nodos, marker={'size': 14, 'color': color_hex}, text=nombres, hoverinfo="text"))
                fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=300, mapbox=dict(style="white-bg", center=centro, zoom=14.5, layers=[{"below": 'traces', "sourcetype": "raster", "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]}]), showlegend=False)
                st.plotly_chart(fig_mapa, use_container_width=True)

# =========================================================
# PILAR 2: SOCIAL Y ECONÓMICO
# =========================================================
elif seccion == "🤝 2. Pilar Social y Económico":
    st.header('''🤝 Pilar 2: Relacionamiento, Confianza y Economía''')
    
    tab_actores, tab_balanza, tab_prioridades = st.tabs([
        "🗺️ Mapeo Dinámico de Actores", 
        "⚖️ Balanza Social (Retos y Potencialidades)", 
        "🎯 Oportunidades y Prioridades del Territorio"
    ])
    
    with tab_actores:
        st.markdown('''<p style='color:#4B5563; margin-bottom: 20px; font-size: 1.1em;'>Clasificación estratégica de los grupos de interés de Aris Mining Marmato según su Nivel de Influencia e Impacto.</p>''', unsafe_allow_html=True)
        
        datos_actores = pd.DataFrame({
            'Grupo de Interés': ['Comunidades Mineras', 'Autoridades Locales', 'Comunidades Locales', 'Colaboradores',
                                 'Autoridades Nacionales', 'Autoridades Regionales', 'Academia y Org.'],
            'Impacto': [4.8, 4.5, 4.6, 3.5, 1.5, 2.0, 2.0],
            'Influencia': [4.5, 4.8, 3.8, 3.2, 4.8, 4.2, 2.0],
            'Cuadrante': ['Relación Cercana', 'Relación Cercana', 'Relación Cercana', 'Relación Cercana',
                          'Mantener Satisfecho', 'Mantener Satisfecho', 'Monitoreo'],
            'Icono': ['⛏️', '🏢', '👥', '👷', '🏛️', '🗺️', '🎓'],
            'Actores': [
                'CMPs (Porvenir, Kabood, MyC, Asoc. Echandía, Alianza), Mesa Minera, Asomitrama, Guacheros.',
                'Alcaldía de Marmato, Personería, Concejo, Policía Nacional.',
                'JACs (9 veredas), Indígenas Cartama, Afro, Asoc. (Mujeres Joyeras, Camacol, LGTBIQA+, Angelitos de Luz).',
                'Empleados directos, Proveedores y Contratistas locales.',
                'ANM, MME, DNP, Procuraduría General.',
                'Gobernación de Caldas, Defensoría, Corpocaldas, ANM PAR.',
                'IEs locales, Universidades (Caldas, EAN, UAM), Bomberos, Hospital, ESPANC.'
            ],
            'Objetivo': [
                'Formalización, minería segura y coexistencia.',
                'Confianza, gobernabilidad y desarrollo integral.',
                'Confianza mediante diálogo e inclusión.',
                'Cultura de seguridad y cadena ASG.',
                'Transparencia, seguridad jurídica y apoyo regulatorio.',
                'Ordenamiento territorial y gestión del riesgo.',
                'Fortalecer capacidades e innovación.'
            ],
            'Aspectos': [
                '• Reducción conflictos empresarial/tradicional.<br>• Fortalecer modelos de coexistencia minera.<br>• Mejora del desempeño social y ambiental.',
                '• Gestión de conflictividad social.<br>• Coordinación institucional para el desarrollo territorial.<br>• Apoyo al modelo de coexistencia minera.',
                '• Identificación temprana de conflictos.<br>• Implementación conjunta de proyectos de inversión social.<br>• Gestión de expectativas.',
                '• Gestión del clima laboral.<br>• Cultura de seguridad y salud en el trabajo.<br>• Prevención de conflictos laborales.',
                '• Gestión de cambios regulatorios y normativos.<br>• Seguridad jurídica.<br>• Apoyo modelo de coexistencia y formalización.',
                '• Gestión del riesgo territorial.<br>• Fortalecimiento institucional.<br>• Coordinación de proyectos estratégicos.<br>• Apoyo a formalización.',
                '• Identificación de oportunidades de innovación.<br>• Fortalecimiento del conocimiento técnico y ASG.<br>• Construcción de alianzas estratégicas.'
            ]
        })
        
        col_espacio_izq, col_grafica, col_espacio_der = st.columns([1, 4, 1])
        
        with col_grafica:
            fig_actores = px.scatter(datos_actores, x='Impacto', y='Influencia', color='Cuadrante',
                                     text='Icono',
                                     color_discrete_map={'Relación Cercana': '#DC2626', 'Mantener Satisfecho': '#2563EB', 'Monitoreo': '#059669'},
                                     custom_data=['Grupo de Interés', 'Actores', 'Objetivo', 'Aspectos'])
            
            fig_actores.update_traces(
                marker=dict(size=65, opacity=0.95, line=dict(width=3, color='white')),
                textfont_size=32, textposition='middle center',
                hovertemplate="<br><b>%{customdata[0]}</b><br><br><b>Actores:</b> %{customdata[1]}<br><br><b>Objetivo:</b> %{customdata[2]}<br><br><b>Aspectos a Gestionar:</b><br>%{customdata[3]}<extra></extra>"
            )
            
            fig_actores.add_shape(type="rect", x0=3, y0=3, x1=5.2, y1=5.2, fillcolor="rgba(220, 38, 38, 0.15)", line=dict(color="#DC2626", width=2), layer="below")
            fig_actores.add_shape(type="rect", x0=0, y0=3, x1=3, y1=5.2, fillcolor="rgba(37, 99, 235, 0.15)", line=dict(color="#2563EB", width=2), layer="below")
            fig_actores.add_shape(type="rect", x0=0, y0=0, x1=3, y1=3, fillcolor="rgba(5, 150, 105, 0.15)", line=dict(color="#059669", width=2), layer="below")
            fig_actores.add_shape(type="rect", x0=3, y0=0, x1=5.2, y1=3, fillcolor="rgba(217, 119, 6, 0.15)", line=dict(color="#D97706", width=2), layer="below")

            fig_actores.add_hline(y=3, line_dash="dash", line_color="#9CA3AF")
            fig_actores.add_vline(x=3, line_dash="dash", line_color="#9CA3AF")
            
            fig_actores.update_xaxes(range=[0, 5.2], title="<b>Nivel de Impacto Recibido (0 a 5)</b>", gridcolor='white')
            fig_actores.update_yaxes(range=[0, 5.2], title="<b>Capacidad de Influencia (0 a 5)</b>", gridcolor='white')
            
            fig_actores.add_annotation(x=0.1, y=5.1, text="MANTENER SATISFECHO", showarrow=False, font=dict(size=12, color="white", weight="bold"), bgcolor="#2563EB", borderpad=5, bordercolor="#1e40af", borderwidth=1, xanchor='left', yanchor='top')
            fig_actores.add_annotation(x=3.1, y=5.1, text="RELACIÓN CERCANA", showarrow=False, font=dict(size=12, color="white", weight="bold"), bgcolor="#DC2626", borderpad=5, bordercolor="#991b1b", borderwidth=1, xanchor='left', yanchor='top')
            fig_actores.add_annotation(x=0.1, y=2.9, text="MONITOREO", showarrow=False, font=dict(size=12, color="white", weight="bold"), bgcolor="#059669", borderpad=5, bordercolor="#065f46", borderwidth=1, xanchor='left', yanchor='top')
            fig_actores.add_annotation(x=3.1, y=2.9, text="MANTENER INFORMADO", showarrow=False, font=dict(size=12, color="white", weight="bold"), bgcolor="#D97706", borderpad=5, bordercolor="#b45309", borderwidth=1, xanchor='left', yanchor='top')
            
            fig_actores.update_layout(height=650, plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Montserrat", color="black"), margin=dict(t=20, l=10, r=10, b=10), showlegend=False)
            st.plotly_chart(fig_actores, use_container_width=True)
            
        st.markdown('''<br>''', unsafe_allow_html=True)
        st.markdown('''#### 📖 Guía Estratégica de Relacionamiento (Cuadrantes)''')
        
        html_quadrants = '''
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; max-width: 900px; margin: 0 auto; padding-bottom: 20px;">
<div style="background: white; border: 1px solid #e5e7eb; border-top: 5px solid #2563EB; border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
<details style="cursor: pointer; outline: none;"><summary style="font-weight: 800; color: #1e3a8a; font-size: 1.05rem; list-style: none;">🔵 Mantener Satisfecho</summary>
<div style="margin-top: 10px; font-size: 0.9rem; color: #4b5563; border-top: 1px dashed #cbd5e1; padding-top: 10px;"><b>(Alta influencia – Bajo impacto)</b><br><br>Grupos con alta capacidad de incidencia sobre decisiones estratégicas y bajo impacto por la operación. Requieren relacionamiento para construir confianza y coordinación institucional.</div></details>
</div>
<div style="background: white; border: 1px solid #e5e7eb; border-top: 5px solid #DC2626; border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
<details style="cursor: pointer; outline: none;"><summary style="font-weight: 800; color: #991b1b; font-size: 1.05rem; list-style: none;">🔴 Relación Cercana</summary>
<div style="margin-top: 10px; font-size: 0.9rem; color: #4b5563; border-top: 1px dashed #cbd5e1; padding-top: 10px;"><b>(Alta influencia – Alto impacto)</b><br><br>Actores con alta capacidad de influir sobre la operación y altos impactos. Prioridad para gestión de riesgos, confianza y desarrollo territorial.</div></details>
</div>
<div style="background: white; border: 1px solid #e5e7eb; border-top: 5px solid #059669; border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
<details style="cursor: pointer; outline: none;"><summary style="font-weight: 800; color: #065f46; font-size: 1.05rem; list-style: none;">🟢 Monitoreo Continuo</summary>
<div style="margin-top: 10px; font-size: 0.9rem; color: #4b5563; border-top: 1px dashed #cbd5e1; padding-top: 10px;"><b>(Baja influencia – Bajo impacto)</b><br><br>Grupos con baja influencia y bajo impacto. Requieren seguimiento continuo para identificar cambios en expectativas o intereses.</div></details>
</div>
<div style="background: white; border: 1px solid #e5e7eb; border-top: 5px solid #D97706; border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
<details style="cursor: pointer; outline: none;"><summary style="font-weight: 800; color: #b45309; font-size: 1.05rem; list-style: none;">🟠 Mantener Informado</summary>
<div style="margin-top: 10px; font-size: 0.9rem; color: #4b5563; border-top: 1px dashed #cbd5e1; padding-top: 10px;"><b>(Baja influencia – Alto impacto)</b><br><br>Grupos con alto impacto por la operación y capacidad de incidencia limitada. Requieren acceso a información oportuna y participación.</div></details>
</div>
</div>
'''
        st.markdown(html_quadrants, unsafe_allow_html=True)

    with tab_balanza:
        st.markdown('''### ⚖️ Potencialidades y Retos en el Territorio (La Balanza Social)''')
        st.markdown('''Síntesis interactiva de los hallazgos en encuestas, entrevistas y cartografía social. *Pica sobre las tarjetas para desplegar los detalles.*''')
        st.divider()

        col_verde, col_kpi = st.columns([3.5, 1])

        with col_verde:
            html_verde = '''
<div class='panel-base'>
<div class='header-verde'>🚦 1. ACTIVOS DE LEGITIMIDAD / FORTALEZAS Y POTENCIALIDADES</div>
<div class='tarjetas-container'>
<details class='tarjeta-btn verde'><summary><div class='t-icono'>🤝</div><div class='t-titulo'>Relacionamiento</div><div class='t-porcentaje-verde'>63%</div><div class='click-hint'>Picar para ver ▼</div></summary><div class='expanded-content'>Aris más abierto al diálogo con la comunidad y autoridades locales.</div></details>
<details class='tarjeta-btn verde'><summary><div class='t-icono'>💵</div><div class='t-titulo'>Economía</div><div class='t-porcentaje-verde'>67%</div><div class='click-hint'>Picar para ver ▼</div></summary><div class='expanded-content'>Sin Aris el empleo y las obras sociales en el territorio estarían peor.</div></details>
<details class='tarjeta-btn verde'><summary><div class='t-icono'>👷</div><div class='t-titulo'>Operación y convivencia</div><div class='t-porcentaje-verde'>66%</div><div class='click-hint'>Picar para ver ▼</div></summary><div class='expanded-content'>Se perciben mejoras significativas en seguridad y salud debido a Aris.</div></details>
<details class='tarjeta-btn verde'><summary><div class='t-icono'>📋</div><div class='t-titulo'>Formalización</div><div class='t-porcentaje-verde'>67%</div><div class='click-hint'>Picar para ver ▼</div></summary><div class='expanded-content'>El modelo de formalización tiene el potencial de transformar Marmato.</div></details>
<details class='tarjeta-btn verde'><summary><div class='t-icono'>🤝</div><div class='t-titulo'>Coexistencia</div><div class='t-porcentaje-verde'>67%</div><div class='click-hint'>Picar para ver ▼</div></summary><div class='expanded-content'>La relación entre la empresa y la minería tradicional ha mejorado.</div></details>
</div>
</div>
'''
            st.markdown(html_verde, unsafe_allow_html=True)

        with col_kpi:
            html_kpi = '''
<div class='panel-kpi'>
<div class='circulo-kpi'>53%</div>
<div class='desc-kpi'>del territorio atribuye el desarrollo actual directamente a Aris Mining.</div>
</div>
'''
            st.markdown(html_kpi, unsafe_allow_html=True)

        st.markdown('''<br>''', unsafe_allow_html=True)

        col_amarillo, col_rojo, col_gi = st.columns([1.6, 1.9, 1])

        with col_amarillo:
            html_amarillo = '''
<div class='panel-base'>
<div class='header-amarillo'>🚦 2. FRICCIONES DE CRECIMIENTO</div>

<div class='tarjetas-container'>
<details class='tarjeta-btn amarillo'>
<summary>
<div class='t-icono'>🏭</div>
<div class='t-titulo'>El Llano</div>
<div class='t-presion'>🔴 Presión Alta</div>
<div class='click-hint'>Picar para ver ▼</div>
</summary>
<div class='expanded-content'>Foco de industrialización y relavera.</div>
</details>

<details class='tarjeta-btn amarillo'>
<summary>
<div class='t-icono'>🚚</div>
<div class='t-titulo'>Echandía</div>
<div class='t-presion'>🔴 Presión Alta</div>
<div class='click-hint'>Picar para ver ▼</div>
</summary>
<div class='expanded-content'>Problemas de tráfico y movilidad constante.</div>
</details>

<details class='tarjeta-btn amarillo'>
<summary>
<div class='t-icono'>⛏️</div>
<div class='t-titulo'>Cien Pesos</div>
<div class='t-presion'>🔴 Presión Alta</div>
<div class='click-hint'>Picar para ver ▼</div>
</summary>
<div class='expanded-content'>Alta concentración de guachería y molinos.</div>
</details>
</div>

<div style="font-size: 0.85rem; color: #374151; padding: 0 15px 15px 15px; margin-top: -5px;">
<p style="margin-bottom: 5px;">• La actividad minera informal atrae población flotante y genera presiones territoriales.</p>
<p style="margin-bottom: 0;">• Gestión con Alcaldía y otros actores. <strong style="color: #92400e;">Aris no puede sola.</strong></p>
</div>
</div>
'''
            st.markdown(html_amarillo, unsafe_allow_html=True)

        with col_rojo:
            html_rojo = '''
<div class='panel-base'>
<div class='header-rojo'>🚦 3. RIESGOS OPERATIVOS REPUTACIONALES</div>
<div class='tarjetas-container'>
<details class='tarjeta-btn rojo'><summary><div class='t-icono'>👥</div><div class='t-titulo'>Relacionamiento</div><div class='t-porcentaje-rojo'>67%</div><div class='click-hint'>Picar para ver ▼</div></summary><div class='expanded-content'>Percepción de beneficios sociales concentrados en pocas personas.</div></details>
<details class='tarjeta-btn rojo'><summary><div class='t-icono'>💵</div><div class='t-titulo'>Economía</div><div class='t-porcentaje-rojo'>67%</div><div class='click-hint'>Picar para ver ▼</div></summary><div class='expanded-content'>Inversión social no está totalmente asociada a problemas del territorio.</div></details>
<details class='tarjeta-btn rojo'><summary><div class='t-icono'>👷</div><div class='t-titulo'>Operación y convivencia</div><div class='t-porcentaje-rojo'>71%</div><div class='click-hint'>Picar para ver ▼</div></summary><div class='expanded-content'>La comunidad exige reglas claras para los procesos de formalización.</div></details>
<details class='tarjeta-btn rojo'><summary><div class='t-icono'>🍃</div><div class='t-titulo'>Territorio y ambiente</div><div class='t-porcentaje-rojo'>67%</div><div class='click-hint'>Picar para ver ▼</div></summary><div class='expanded-content'>Percibe que el manejo del agua, suelo y paisaje ha empeorado.</div></details>
</div>
</div>
'''
            st.markdown(html_rojo, unsafe_allow_html=True)

        with col_gi:
            html_gi = '''
<div class='gi-container'>
<div class='gi-titulo'>Percepciones por G.I</div>
<details class='tarjeta-btn gi'><summary><div style='display:flex; align-items:center; gap:10px;'><span style='font-size:1.2rem;'>👷</span><b style='color:#0087a3; font-size:0.85rem;'>Mineros tradicionales</b></div></summary><div class='expanded-content' style='text-align: left; margin-top:5px; padding-top:5px;'>Esperan y demandan <strong>reglas claras</strong>.</div></details>
<details class='tarjeta-btn gi'><summary><div style='display:flex; align-items:center; gap:10px;'><span style='font-size:1.2rem;'>👔</span><b style='color:#0087a3; font-size:0.85rem;'>Colab. y Autoridades</b></div></summary><div class='expanded-content' style='text-align: left; margin-top:5px; padding-top:5px;'>Son los más optimistas, <strong>destacan la gestión</strong>.</div></details>
<details class='tarjeta-btn gi'><summary><div style='display:flex; align-items:center; gap:10px;'><span style='font-size:1.2rem;'>👥</span><b style='color:#0087a3; font-size:0.85rem;'>Hogares y comunidad</b></div></summary><div class='expanded-content' style='text-align: left; margin-top:5px; padding-top:5px;'>Son los <strong>más críticos</strong> de la gestión actual.</div></details>
</div>
'''
            st.markdown(html_gi, unsafe_allow_html=True)

    with tab_prioridades:
        st.markdown('''#### 🎯 Prioridades y Oportunidades del Territorio''')
        st.markdown('''<span style='font-size: 0.9rem; color: #4b5563;'>Cruce analítico entre la urgencia de necesidades locales y el nivel de reconocimiento de gestión.</span>''', unsafe_allow_html=True)
        st.divider()

        # 1. Gráfico de Barras Estilo Infográfico interactivo
        st.markdown('''#### 🗣️ ¿Qué está pidiendo el territorio?''')
        
        fig_bar = go.Figure()
        
        fig_bar.add_trace(go.Bar(
            x=datos_prioridades['Proporción'],
            y=datos_prioridades['Temas Prioritarios'],
            orientation='h',
            marker_color=datos_prioridades['Color'],
            text=datos_prioridades['Proporción'].astype(str) + '%',
            textposition='inside',
            insidetextanchor='end',
            textfont=dict(color='white', size=14, weight='bold'),
            customdata=datos_prioridades[['Tema_Corto', 'Explicacion']],
            hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br><br><b>Proporción: %{x}%</b><extra></extra>"
        ))
        
        fig_bar.add_trace(go.Scatter(
            x=[18.5] * len(datos_prioridades), 
            y=datos_prioridades['Temas Prioritarios'],
            mode='markers+text',
            marker=dict(size=40, color='#e2e8f0', line=dict(color='white', width=0)),
            text=datos_prioridades['Orden'],
            textfont=dict(size=16, color='#1e3a8a', family='Montserrat', weight='bold'),
            hoverinfo='none'
        ))
        
        fig_bar.update_layout(
            height=450, 
            plot_bgcolor='rgba(0,0,0,0)', 
            xaxis_title="Proporción de Recomendaciones (%)", 
            yaxis_title="",
            margin=dict(l=10, r=20, t=20, b=20),
            showlegend=False
        )
        fig_bar.update_xaxes(showgrid=True, gridcolor='#e5e7eb', range=[0, 20])
        fig_bar.update_yaxes(autorange="reversed", tickfont=dict(size=13)) 
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.divider()
        
        # 2. Matriz de Oportunidades 
        st.markdown('''#### 🔲 Matriz de Oportunidad Territorial''')
        
        col_matriz, col_cats = st.columns([2.8, 1])
        
        with col_matriz:
            fig_matrix = go.Figure()
            
            for idx, row in datos_matriz.iterrows():
                fig_matrix.add_trace(go.Scatter(
                    x=[row['Reconocimiento']],
                    y=[row['Necesidad']],
                    mode='markers+text',
                    marker=dict(size=65, color=row['Color'], opacity=1.0, line=dict(width=3, color='white')),
                    text=[row['Icono']],
                    textfont=dict(size=28, color='white'),
                    name=row['Iniciativa'],
                    customdata=[[row['Iniciativa'], row['Leyenda']]],
                    hovertemplate="<b>%{customdata[0]}</b><br>Estado / Porcentaje: <b>%{customdata[1]}</b><extra></extra>"
                ))

            fig_matrix.add_shape(type="rect", x0=0, x1=5, y0=5, y1=10, fillcolor="rgba(225, 54, 79, 0.1)", line=dict(color="#e1364f", width=2), layer="below")
            fig_matrix.add_shape(type="rect", x0=5, x1=10, y0=5, y1=10, fillcolor="rgba(40, 167, 69, 0.1)", line=dict(color="#28a745", width=2), layer="below")
            fig_matrix.add_shape(type="rect", x0=0, x1=5, y0=0, y1=5, fillcolor="rgba(142, 68, 173, 0.1)", line=dict(color="#8e44ad", width=2), layer="below")
            fig_matrix.add_shape(type="rect", x0=5, x1=10, y0=0, y1=5, fillcolor="rgba(0, 137, 123, 0.1)", line=dict(color="#00897b", width=2), layer="below")

            fig_matrix.add_hline(y=5, line_width=3, line_dash="solid", line_color="white")
            fig_matrix.add_vline(x=5, line_width=3, line_dash="solid", line_color="white")
            
            fig_matrix.add_annotation(x=0.2, y=9.8, text="<b>DESAFÍOS CRÍTICOS</b>", showarrow=False, font=dict(color="white", size=12), bgcolor="#e1364f", borderpad=5, borderwidth=1, bordercolor="white", xanchor='left', yanchor='top')
            fig_matrix.add_annotation(x=9.8, y=9.8, text="<b>OPORTUNIDADES ESTRATÉGICAS</b>", showarrow=False, font=dict(color="white", size=12), bgcolor="#28a745", borderpad=5, borderwidth=1, bordercolor="white", xanchor='right', yanchor='top')
            fig_matrix.add_annotation(x=0.2, y=0.2, text="<b>SEGUIMIENTO Y FORTALECIMIENTO</b>", showarrow=False, font=dict(color="white", size=12), bgcolor="#8e44ad", borderpad=5, borderwidth=1, bordercolor="white", xanchor='left', yanchor='bottom')
            fig_matrix.add_annotation(x=9.8, y=0.2, text="<b>ACTIVOS A CONSOLIDAR</b>", showarrow=False, font=dict(color="white", size=12), bgcolor="#00897b", borderpad=5, borderwidth=1, bordercolor="white", xanchor='right', yanchor='bottom')

            fig_matrix.update_layout(
                height=600, 
                plot_bgcolor='rgba(0,0,0,0)', 
                xaxis_title="← Bajo | Reconocimiento de la contribución de Aris Mining | Alto →", 
                yaxis_title="← Baja | Necesidad Territorial | Alta →", 
                showlegend=False,
                margin=dict(t=20, b=40, l=40, r=20)
            )
            fig_matrix.update_xaxes(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False)
            fig_matrix.update_yaxes(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False)
            
            st.plotly_chart(fig_matrix, use_container_width=True)

        with col_cats:
            html_categorias = '''
<div style="font-family: Montserrat;">
<div style="font-weight: 800; font-size: 1rem; color: #1f2937; margin-bottom: 20px; border-bottom: 3px solid #1E3A8A; padding-bottom: 5px;">📘 Mensajes Clave</div>

<details class="cat-btn cat-btn-red">
<summary>🔴 Desafíos Críticos</summary>
<div class="cat-content">
El agua, el ambiente y la convivencia minera son las principales alertas reputacionales. La presión sobre los servicios públicos requiere gestión urgente.
</div>
</details>

<details class="cat-btn cat-btn-green">
<summary>🟢 Op. Estratégicas</summary>
<div class="cat-content">
La formalización minera es la gran oportunidad para el territorio. La inclusión de mujeres y jóvenes es clave para la licencia social a largo plazo.
</div>
</details>

<details class="cat-btn cat-btn-blue">
<summary>🔵 Activos a Consolidar</summary>
<div class="cat-content">
El empleo generado, las mejoras en seguridad minera y la apertura al diálogo son los mayores activos de legitimidad. Deben mantenerse.
</div>
</details>

<details class="cat-btn cat-btn-purple">
<summary>🟣 Seguimiento</summary>
<div class="cat-content">
Aspectos como la cobertura de la inversión social y la infraestructura básica requieren un monitoreo constante para no convertirse en pasivos futuros.
</div>
</details>

<div style="margin-top: 30px; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px; text-align: center;">
<div style="font-size: 2rem;">👆</div>
<div style="font-size: 0.8rem; color: #6b7280; font-weight: 600; margin-top: 5px;">Pasa el cursor sobre los íconos o las barras para ver sus detalles interactivos.</div>
</div>
</div>
'''
            st.markdown(html_categorias, unsafe_allow_html=True)

# =========================================================
# PILAR 3: GOBERNANZA 
# =========================================================
elif seccion == "⚖️ 3. Pilar Gobernanza":
    st.header('''⚖️ Pilar 3: Gobernanza y Formalización Minera''')
    st.info('''**Hallazgo Clave:** La formalización es el corazón estratégico. El 71% del territorio exige reglas claras para la convivencia entre la minería empresarial y la tradicional.''')
    
    tab_eco, tab_ejes = st.tabs(["⚙️ Modelo Socios Mineros", "🗺️ 6 Brechas y 10 Lecciones (Hoja de Ruta)"])
    
    with tab_eco:
        html_cmp = '''
<div class="rel-main-container" style="min-height: auto;">
<div class="rel-left" style="background: #854d0e;">
<h2>Modelo Socios Mineros</h2>
<p>Minería con legalidad, oportunidades y desarrollo para el territorio.</p>
<blockquote style="border-left-color: #fcd34d; color: #fef3c7;">"Una minería responsable fortalece a las personas y construye futuro."</blockquote>
</div>
<div class="rel-right" style="padding: 20px;">
<div style="display:flex; gap:15px; margin-bottom: 20px;">
<div style="flex:1; background:#f8fafc; padding:15px; border-radius:8px; border:1px solid #e2e8f0; text-align:center;">
<div style="font-size:2rem; margin-bottom:5px;">✅</div><div style="font-weight:bold; color:#1e3a8a;">Minería Legal</div><div style="font-size:0.8rem; color:#64748b;">Cumplimiento normativo</div>
</div>
<div style="flex:1; background:#f8fafc; padding:15px; border-radius:8px; border:1px solid #e2e8f0; text-align:center;">
<div style="font-size:2rem; margin-bottom:5px;">👷</div><div style="font-weight:bold; color:#1e3a8a;">Minería Segura</div><div style="font-size:0.8rem; color:#64748b;">Mejores prácticas SST</div>
</div>
<div style="flex:1; background:#f8fafc; padding:15px; border-radius:8px; border:1px solid #e2e8f0; text-align:center;">
<div style="font-size:2rem; margin-bottom:5px;">🍃</div><div style="font-weight:bold; color:#1e3a8a;">Minería Responsable</div><div style="font-size:0.8rem; color:#64748b;">Respeto ambiental</div>
</div>
</div>

<details class="mech-details"><summary><span class="mech-num" style="background:#10b981;">🌟</span> Fortalezas del Modelo (La Maruja)</summary>
<div class="mech-desc">
<ul style="margin-bottom:0;">
<li><b>Coexistencia Operativa:</b> 4 operadores organizados.</li>
<li><b>Cadena articulada:</b> Explotación, transporte y beneficio.</li>
<li><b>Consistencia ambiental:</b> Percolación autorizada.</li>
<li><b>Aprendizaje:</b> Las prácticas de seguridad minera de Aris son imitadas por iniciativa propia en el territorio.</li>
</ul>
</div></details>

<details class="mech-details"><summary><span class="mech-num" style="background:#f59e0b;">⚠️</span> Oportunidades de Mejora</summary>
<div class="mech-desc">
<ul style="margin-bottom:0;">
<li><b>Responsabilidades claras:</b> Evitar dilución titular-operador.</li>
<li><b>Cumplimiento documentado:</b> Matriz de obligaciones.</li>
<li><b>Evaluación independiente:</b> Seguridad y trazabilidad.</li>
<li><b>Replicabilidad:</b> Asegurar condiciones técnicas antes de expandir.</li>
</ul>
</div></details>
</div>
</div>
'''
        st.markdown(html_cmp, unsafe_allow_html=True)

    with tab_ejes:
        html_ejes = '''
<div class="rel-main-container" style="min-height: auto;">
<div class="rel-left" style="background: #1e3a8a;">
<h2>Brechas y Lecciones</h2>
<p>La formalización no es solo entregar títulos. Requiere superar barreras estructurales e incorporar buenas prácticas internacionales.</p>
</div>
<div class="rel-right" style="padding: 30px;">
<h4 style="color:#1e3a8a; margin-bottom:15px; font-weight:700;">🚧 6 Brechas de Formalización a superar en Marmato</h4>

<details class="mech-details"><summary><span class="mech-num" style="background:#3b82f6;">1</span><span class="mech-icon">⚖️</span> Brecha Jurídica y Propiedad</summary>
<div class="mech-desc">Superposición de áreas, conflicto entre catastro (suelo) y títulos (subsuelo). No todas las Unidades Productivas Mineras (UPM) pueden acceder a la misma figura.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#f59e0b;">2</span><span class="mech-icon">⚙️</span> Brecha Técnico-Minera</summary>
<div class="mech-desc">Falta información técnica del estado real de las labores: reservas remanentes, estabilidad de bocaminas, subsidencia, ventilación y manejo de explosivos.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#10b981;">3</span><span class="mech-icon">🍃</span> Brecha Ambiental</summary>
<div class="mech-desc">Ausencia de datos integrados para control de vertimientos, disposición de estériles y protección de cuencas en el proceso de formalización colectiva.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#ef4444;">4</span><span class="mech-icon">⚠️</span> Brecha de Gestión del Riesgo</summary>
<div class="mech-desc">Alta concentración de UPM en zonas de amenaza alta por deslizamiento que requieren estudios geotécnicos preventivos antes de formalizar.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#8b5cf6;">5</span><span class="mech-icon">💰</span> Brecha Económica</summary>
<div class="mech-desc">Si la formalización se exige como imposición sin conectar financiamiento, beneficio de mineral y comercialización formal, fracasará por costos operativos.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#06b6d4;">6</span><span class="mech-icon">🏛️</span> Brecha Institucional</summary>
<div class="mech-desc">Leyes avanzadas sin capacidad local. Requiere articulación urgente entre ANM, Alcaldía, Corpocaldas y Aris Mining para no ser un mero "trámite en papel".</div></details>

<div style="margin-top: 25px; padding: 15px; background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px;">
<details class="mech-details" style="margin-bottom:0;"><summary><span class="mech-icon">🌎</span> Decálogo de Lecciones Internacionales Aprendidas</summary>
<div class="mech-desc" style="font-size:0.85rem;">
<b>1.</b> Formalizar no es solo entregar títulos.<br>
<b>2.</b> La legalidad debe ser económicamente viable (costos proporcionales).<br>
<b>3.</b> El comprador formal es tan importante como la autoridad minera.<br>
<b>4.</b> La planta de beneficio es el cuello de botella crítico del oro.<br>
<b>5.</b> La trazabilidad debe empezar en la mina, no en la exportación.<br>
<b>6.</b> La organización colectiva reduce costos y mejora control.<br>
<b>7.</b> La fiscalización debe combinar incentivos y sanciones.<br>
<b>8.</b> Diferenciar tipos de mineros (no todos son iguales).<br>
<b>9.</b> El enfoque territorial y de uso de suelo es indispensable.<br>
<b>10.</b> El éxito requiere permanencia institucional, no solo "pilotos".
</div></details>
</div>
</div>
</div>
'''
        st.markdown(html_ejes, unsafe_allow_html=True)

# =========================================================
# PILAR 4: INFORMACIÓN 
# =========================================================
elif seccion == "📡 4. Pilar Información":
    st.header('''📡 Pilar 4: Sistemas de Monitoreo e Información (Centro de Inteligencia Transparente)''')
    st.markdown('''**Propuesta de Valor:** Para generar impacto real y construir legitimidad, este pilar no debe ser solo un archivo de datos, sino una plataforma de transparencia abierta a la comunidad. Se estructura en tres ejes fundamentales:''')
    
    html_p4 = '''
<div class="rel-main-container">
<div class="rel-left" style="background: #0f766e;">
<h2>Centro de Inteligencia Transparente</h2>
<p>Plataforma abierta para generar legitimidad basada en datos reales, verificables y de acceso comunitario.</p>
<blockquote style="border-left-color: #5eead4; color: #ccfbf1;">"La transparencia elimina la desconfianza ambiental."</blockquote>
</div>
<div class="rel-right" style="padding: 30px;">
<h4 style="color:#115e59; margin-bottom:15px; font-weight:700;">Ejes de Monitoreo Territorial</h4>

<details class="mech-details"><summary><span class="mech-num" style="background:#0ea5e9;">1</span><span class="mech-icon">💧</span> Monitoreo Participativo (Agua y Aire)</summary>
<div class="mech-desc">Red continua y en tiempo real en quebradas críticas (Cascabel, Pantanos). Los datos deben ser accesibles y validados junto a la comunidad para eliminar la desconfianza ambiental generada por terceros o impactos acumulativos.</div></details>

<details class="mech-details"><summary><span class="mech-num" style="background:#10b981;">2</span><span class="mech-icon">🗺️</span> SIG Minero-Ambiental (Georreferenciación)</summary>
<div class="mech-desc">Georreferenciación interactiva de la operación, pasivos ambientales, taludes y subsidencia. Permite identificar zonas de amenaza alta y coordinar acciones de reubicación o mitigación directa con la Alcaldía Municipal y Corpocaldas.</div></details>

<details class="mech-details"><summary><span class="mech-num" style="background:#8b5cf6;">3</span><span class="mech-icon">📊</span> Rendición de Cuentas CSR (Inversión)</summary>
<div class="mech-desc">Tablero de seguimiento a la Inversión Social (vías, escuelas, alianzas). Trasladar los datos <i>"de la actividad al resultado"</i> para que el territorio verifique el impacto real, el presupuesto y el avance de cada proyecto comunitario.</div></details>
</div>
</div>
'''
    st.markdown(html_p4, unsafe_allow_html=True)

# =========================================================
# PILAR 5: SOSTENIBILIDAD
# =========================================================
elif seccion == "♻️ 5. Pilar Sostenibilidad":
    st.header('''♻️ Pilar 5: Sostenibilidad y Creación de Valor''')
    st.markdown('''Alineación con estándares ASG para priorizar la inversión social, garantizar impactos a largo plazo y construir legitimidad mediante el diálogo.''')
    
    tab_rel, tab_prio, tab_linea = st.tabs(["🗣️ Estrategia de Relacionamiento Territorial", "📊 Priorización de Inversión", "⏳ Línea de Tiempo"])
    
    with tab_rel:
        rel_html = '''
<div class="rel-main-container">
<div class="rel-left" style="background: #0f3f71;">
<h2>Estrategia de Relacionamiento Territorial</h2>
<p>Sistema de identificación temprana de riesgos, gestión de expectativas y construcción de legitimidad en el territorio.</p>
<blockquote>"El diálogo abre territorios más fuertes."</blockquote>
</div>
<div class="rel-right" style="padding: 30px;">
<div class="rel-obj-container">
<div class="rel-obj">
<div class="rel-obj-num">1</div>
<div class="rel-obj-title">Entender y priorizar</div>
<div class="rel-obj-desc">las necesidades, expectativas y percepciones del territorio y sus actores clave.</div>
</div>
<div class="rel-obj">
<div class="rel-obj-num" style="background:#10b981;">2</div>
<div class="rel-obj-title" style="color:#047857;">Gestionar y documentar</div>
<div class="rel-obj-desc">los procesos de gestión de impactos e inversión social en el territorio.</div>
</div>
<div class="rel-obj">
<div class="rel-obj-num" style="background:#f59e0b;">3</div>
<div class="rel-obj-title" style="color:#b45309;">Medir la percepción</div>
<div class="rel-obj-desc">de Aris en el territorio en el mediano y largo plazo.</div>
</div>
</div>
<h4 style="color:#1e3a8a; margin-bottom:15px; font-weight:700;">Mecanismos de relacionamiento</h4>
<details class="mech-details"><summary><span class="mech-num" style="background:#3b82f6;">1</span><span class="mech-icon">💧</span> Mesa ambiental y del agua</summary>
<div class="mech-desc">Monitorear el agua y el ambiente, revisando impactos, indicadores y compromisos.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#10b981;">2</span><span class="mech-icon">🚚</span> Comité de movilidad y transporte</summary>
<div class="mech-desc">Seguimiento a rutas y horarios para prevenir impactos viales, polvo y ruido.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#f59e0b;">3</span><span class="mech-icon">👥</span> Ciclo de diálogo con JAC</summary>
<div class="mech-desc">Recoger aportes de las comunidades frente a proyectos e intervenciones.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#ef4444;">4</span><span class="mech-icon">📋</span> Mecanismo de PQRS</summary>
<div class="mech-desc">Recibir, responder y cerrar casos con trazabilidad y análisis de tendencias.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#8b5cf6;">5</span><span class="mech-icon">🗣️</span> Espacios de socialización</summary>
<div class="mech-desc">Priorizar compromisos, informar avances y recoger retroalimentación de la gestión.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#06b6d4;">6</span><span class="mech-icon">⚙️</span> Convenios de verificación técnica</summary>
<div class="mech-desc">Evaluación independiente de impactos y compromisos para fortalecer credibilidad.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#f97316;">7</span><span class="mech-icon">📊</span> Rendición pública de cuentas</summary>
<div class="mech-desc">Transparentar los avances y resultados de la inversión social y desarrollo de proyectos.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#0284c7;">8</span><span class="mech-icon">🔍</span> Medición de percepciones</summary>
<div class="mech-desc">Identificar brechas, ajustar la gestión y hacer seguimiento a su evolución.</div></details>
</div>
</div>
'''
        st.markdown(rel_html, unsafe_allow_html=True)
    
    with tab_prio:
        html_prio = '''
<div class="rel-main-container" style="min-height: auto;">
<div class="rel-left" style="background: #1d4ed8;">
<h2>Priorización de la Inversión</h2>
<p>Invertir con sentido territorial hoy, construye oportunidades reales mañana.</p>
<blockquote style="border-left-color: #93c5fd; color: #dbeafe;">"Priorizar es multiplicar el impacto."</blockquote>
</div>
<div class="rel-right" style="padding: 30px;">
<details class="mech-details"><summary><span class="mech-num" style="background:#3b82f6;">1</span><span class="mech-icon">🎯</span> Responde a Necesidades Reales</summary>
<div class="mech-desc">Se basa en diagnósticos ambientales, sociales, económicos y de gobernanza del territorio.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#10b981;">2</span><span class="mech-icon">📈</span> Genera Mayor Impacto y Efectividad</summary>
<div class="mech-desc">Concentra esfuerzos en proyectos que producen resultados medibles y sostenibles.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#f59e0b;">3</span><span class="mech-icon">💰</span> Optimiza el Uso de los Recursos</summary>
<div class="mech-desc">Prioriza iniciativas viables y estratégicas, evitando la dispersión de esfuerzos.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#ef4444;">4</span><span class="mech-icon">🤝</span> Fortalece la Confianza y la Legitimidad</summary>
<div class="mech-desc">Responde a las expectativas de las comunidades y se construye con participación y transparencia.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#8b5cf6;">5</span><span class="mech-icon">🌱</span> Contribuye a la Sostenibilidad del Negocio</summary>
<div class="mech-desc">Reduce riesgos sociales, fortalece la licencia social y crea condiciones para la continuidad operativa.</div></details>
</div>
</div>
'''
        st.markdown(html_prio, unsafe_allow_html=True)

    with tab_linea:
        html_linea = '''
<div class="rel-main-container" style="min-height: auto;">
<div class="rel-left" style="background: #4338ca;">
<h2>Hoja de Ruta y Línea de Tiempo</h2>
<p>Relaciones que hoy construyen territorios sostenibles mañana.</p>
<blockquote style="border-left-color: #a5b4fc; color: #e0e7ff;">"Avanzar juntos es hacer posible un territorio con más oportunidades."</blockquote>
</div>
<div class="rel-right" style="padding: 30px;">
<details class="mech-details"><summary><span class="mech-num" style="background:#3b82f6;">1</span><span class="mech-icon">🔍</span> Corto Plazo (0-1 Año): Conocer y Priorizar</summary>
<div class="mech-desc">Entender el territorio, sus actores y necesidades clave. Diagnóstico y escucha activa como base de la acción.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#10b981;">2</span><span class="mech-icon">👥</span> Mediano Plazo (1-3 Años): Construir Juntos</summary>
<div class="mech-desc">Diseñar e implementar iniciativas con participación del territorio. Corresponsabilidad y alianzas para el desarrollo.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#f59e0b;">3</span><span class="mech-icon">⚙️</span> Mediano Plazo (1-3 Años): Fortalecer Capacidades</summary>
<div class="mech-desc">Impulsar capacidades locales, inclusión y oportunidades sostenibles. Comunidades más preparadas y con más oportunidades.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#0f766e;">4</span><span class="mech-icon">📈</span> Largo Plazo (3+ Años): Consolidar Resultados</summary>
<div class="mech-desc">Medir, ajustar y escalar lo que genera mayor impacto. Resultados visibles y sostenibles en el territorio.</div></details>
<details class="mech-details"><summary><span class="mech-num" style="background:#4338ca;">5</span><span class="mech-icon">🏔️</span> Futuro Compartido: Territorios más fuertes</summary>
<div class="mech-desc">Comunidades prósperas, relaciones de confianza, bienestar, oportunidades y un territorio sostenible.</div></details>
</div>
</div>
'''
        st.markdown(html_linea, unsafe_allow_html=True)
