# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 14:27:46 2022

@author: Franco Fabián
Últiva modificación: Feb 24 2022
"""
'''
    Área: Unidad de Planificación y Presupuesto - Equipo Data
    Objetivos: Costear Secundaria con Residencia Estudiantil 2022

        ETAPA 0: Preparar e importar librerías

        ETAPA 1: Definir variables para remuneración

            a) Períodos de tiempo
            b) Remuneraciones

        ETAPA 2: Generar Padrón SRE

            a) Importar Padrón Escale e Intervención
            b) Exportar Padrón SRE

        ETAPA 3: Cálculo del PxQ

            a) Cálculo de contratación CAS
            b) Cálculo de EsSalud
            c) Cálculo de montos totales
            d) Exportar componentes del PxQ

        ETAPA 4: Base SIAF (formato MINEDU)

        ETAPA 5: Base SIAF (formato MEF)

'''

'''
        ETAPA 0: Preparar e importar librerías

'''

# Ruta del directorio: D:\upp

ruta='D:\SRE_2022'

# Ruta de archivos de entrada: D:\upp\Input

ruta_input=ruta+'\Input'

# Ruta de archivos de salida: D:\upp\Output

ruta_output=ruta+'\Output'

# Importar librería Pandas

import pandas as pd

# Importar librería dbfread

from dbfread import DBF

'''
        ETAPA 1: Definir variables para remuneración

'''

# a) Períodos de tiempo

# Continuidad: 12 meses

meses_ano12=12

# Nuevos contratos: 10 meses

meses_ano10=10

# Meses total

meses_total=['ene','feb','mar','abr','may','jun','jul','ago','set','oct','nov','dic']

# Meses continuidad

meses_activo12=['ene','feb','mar','abr','may','jun','jul','ago','set','oct','nov','dic']

# Meses nuevos contratos

meses_activo10=['mar','abr','may','jun','jul','ago','set','oct','nov','dic']
meses_inactivo10=['ene','feb']

# Meses con aguinaldo

meses_agui2=['jul','dic']
meses_sinagui2=['ene','feb','mar','abr','may','jun','ago','set','oct','nov']

# b) Remuneraciones

# Monto Coordinadores de Residencia

monto_coor=2500

# Monto Gestores Educativos

monto_gest=1400

# Monto Promotores de bienestar

monto_prom=1400

# Monto personal de cocina

monto_coci=1000

# Monto personal de limpieza

monto_limp=1000

# Monto personal de seguridad

monto_segu=1000

# MResponsable de bienestar SRE

monto_resp=2500

# Monto aguinaldo 1 o 2 veces al año

monto_agui=300

# Valor proyectado de UIT para el 2022

UIT_2022=4600

# Porcentaje para monto techo en EsSalud CAS

UIT_porc=0.55

'''
        ETAPA 2: Generar Padrón SRE

'''

# a) Importar Padrón Escale e Intervención

# Importar Padrón SRE continuidad

pad_cont = pd.read_excel(ruta_input+ "/Padron_sre_cont.xlsx",sheet_name='Hoja1',nrows=75,header=0)

# Renombrar Código Modular

pad_cont.rename(columns={'Código Modular':'cod_mod'},inplace=True)

# Importar base Integrada

#bas_int=pd.read_stata(ruta_input+'/base_integrada_cod_mod.dta')

# Filtrar para estado igual a activa IE

#bas_int = bas_int[bas_int.d_estado == 'Activa']

# Establecer df con variables de interés

#bas_int_i=bas_int[['cod_mod','codooii','codlocal','anexo','cen_edu']]

# Verificar tipo de variables

#print(bas_int_i.dtypes)

# Pasar a integer

#bas_int_i.cod_mod=bas_int_i.cod_mod.astype(int)

# Importar Padrón web

# Generar DBF

b_dbf=DBF(ruta_input+'/Padron_web_20220314.dbf')

# Generar dataframe

pad_web = pd.DataFrame(iter(b_dbf))

# Filtrar para estado igual a activa IE

pad_web = pad_web[pad_web.D_ESTADO == 'Activa']

# Establecer df con variables de interés

pad_web_i=pad_web[['COD_MOD','CODOOII','CODLOCAL','ANEXO','CEN_EDU']]

# Verificar tipo de variables

print(pad_web_i.dtypes)

# Pasar a integer

pad_web_i.COD_MOD=pad_web_i.COD_MOD.astype(int)

# Renombrar variables

pad_web_i.rename(columns={'COD_MOD':'cod_mod'},inplace=True)
pad_web_i.rename(columns={'CODOOII':'codooii'},inplace=True)
pad_web_i.rename(columns={'CODLOCAL':'codlocal'},inplace=True)
pad_web_i.rename(columns={'ANEXO':'anexo'},inplace=True)
pad_web_i.rename(columns={'CEN_EDU':'cen_edu'},inplace=True)

# Combinar bases usando inner

cont_int=pd.merge(pad_cont, pad_web_i, on ='cod_mod', how ='inner')

# Renombrar variables

cont_int.rename(columns={'Código Pliego':'cod_pliego'},inplace=True)
cont_int.rename(columns={'Pliego ':'nom_pliego'},inplace=True)
cont_int.rename(columns={'Código de Ejecutora':'cod_ue'},inplace=True)
cont_int.rename(columns={'Unidad ejecutora':'nom_ue'},inplace=True)
cont_int.rename(columns={'codooii':'cod_ugel'},inplace=True)
cont_int.rename(columns={'Ugel':'ugel'},inplace=True)
cont_int.rename(columns={'Total de estudiantes (SIAGIE 31/08)':'n_estudiantes'},inplace=True)
cont_int.rename(columns={'Testudiantes_residentes':'n_estu_resi'},inplace=True)
cont_int.rename(columns={'Testudiantes_no_residentes':'n_estu_noresi'},inplace=True)
cont_int.rename(columns={'Testudiantes_residentes_hom':'n_estu_resi_m'},inplace=True)
cont_int.rename(columns={'Testudiantes_residentes_muj':'n_estu_resi_f'},inplace=True)
cont_int.rename(columns={'codlocal':'cod_local'},inplace=True)

# Importar base AIRSHP

bas_air = pd.read_excel(ruta_input+'/Anexo_PEAS_continuidad_2022_AIRSHP.xlsx',sheet_name='PEAS_2021_Esc_continuidad',header=1,engine='openpyxl')

# Renombrar variables

bas_air.rename(columns={'Intervención':'intervencion'},inplace=True)
bas_air.rename(columns={'Cargo':'cargo'},inplace=True)
bas_air.rename(columns={'Código modular':'cod_mod'},inplace=True)

# Verificar tipo de variables

print(bas_air.dtypes)

# Eliminar valores nan

bas_air = bas_air.dropna()

# Pasar a integer

bas_air.cod_mod=bas_air.cod_mod.astype(int)

# Mantener solo intervención igual a Implementación de la Secundaria con Residencia Estudiantil

bas_air = bas_air[bas_air.intervencion == 'Implementación de la Secundaria con Residencia Estudiantil']

# Generar variable PEAS por perfil

bas_air.loc[(bas_air['cargo']=='Coordinador(a) de residencia estudiantil')&(bas_air['Contratado_airshp']==1),'n_coor_cont'] = '1'
bas_air.loc[(bas_air['cargo']=='Personal de cocina')&(bas_air['Contratado_airshp']==1),'n_coci_cont'] = '1'
bas_air.loc[(bas_air['cargo']=='Personal de limpieza y mantenimiento')&(bas_air['Contratado_airshp']==1),'n_limp_cont'] = '1'
bas_air.loc[(bas_air['cargo']=='Personal de seguridad')&(bas_air['Contratado_airshp']==1),'n_segu_cont'] = '1'
bas_air.loc[(bas_air['cargo']=='Promotor(a) de Bienestar')&(bas_air['Contratado_airshp']==1),'n_prom_cont'] = '1'
bas_air.loc[(bas_air['cargo']=='Responsable de bienestar SRE')&(bas_air['Contratado_airshp']==1),'n_resp_cont'] = '1'

# Reemplazar nan por 0

bas_air = bas_air.fillna(0)

# Verificar tipo de variables

print(bas_air.dtypes)

# Pasar a int

bas_air.n_coor_cont=bas_air.n_coor_cont.astype(int)
bas_air.n_coci_cont=bas_air.n_coci_cont.astype(int)
bas_air.n_limp_cont=bas_air.n_limp_cont.astype(int)
bas_air.n_segu_cont=bas_air.n_segu_cont.astype(int)
bas_air.n_prom_cont=bas_air.n_prom_cont.astype(int)
bas_air.n_resp_cont=bas_air.n_resp_cont.astype(int)

# Agrupar a nivel de cod_mod (collapse)

bas_airg=bas_air.groupby(['cod_mod'])[['n_coor_cont','n_coci_cont','n_limp_cont','n_segu_cont','n_prom_cont','n_resp_cont']].sum()

# Combinar bases usando inner

base_intermedia=pd.merge(bas_airg, cont_int, on ='cod_mod', how ="inner")

# Generar padron SRE

pad_sre_2022=base_intermedia[['nom_pliego','nom_ue','ugel','cod_mod','anexo','cod_local','cen_edu']]

# b) Exportar Padrón SRE

pad_sre_2022.to_excel(ruta_output+'/base_padron_SRE_2302.xlsx', sheet_name='nombre' , index= False)

'''
        ETAPA 3: Cálculo del PxQ

'''

# a) Cálculo de contratación CAS

# 1. Coordinadores de residencia - 10 meses x 2,500

# Calcular CAS total de Coordinadores de Residencia

base_intermedia['cas_coor_total'] = base_intermedia['Coordinadores de Residencia']*monto_coor*meses_ano10

# Calcular aguinaldo total de Coordinadores de Residencia

base_intermedia['agui_coor_total'] = base_intermedia['Coordinadores de Residencia']*monto_agui*2

# Calcular CAS total por mes de Coordinadores de Residencia

# Meses activo

for mes in meses_activo10:
    base_intermedia['cas_coor_'+mes] = base_intermedia['Coordinadores de Residencia']*monto_coor

# Meses inactivo

for mes in meses_inactivo10:
    base_intermedia['cas_coor_'+mes] = 0

# Calcular aguinaldo total por mes de Coordinadores de Residencia

# Meses con aguinaldo

for mes in meses_agui2:
    base_intermedia['agui_coor_'+mes] = base_intermedia['Coordinadores de Residencia']*monto_agui

# Meses sin aguinaldo

for mes in meses_sinagui2:
    base_intermedia['agui_coor_'+mes] = 0

# 2.1 Responsable de bienestar continuidad - 12 meses x 2,500

# Calcular CAS total de C_Responsable de bienestar SRE

base_intermedia['cas_resp_cont_total'] = base_intermedia['C_Responsable de bienestar SRE']*monto_resp*meses_ano12

# Calcular aguinaldo total de C_Responsable de bienestar SRE

base_intermedia['agui_resp_cont_total'] = base_intermedia['C_Responsable de bienestar SRE']*monto_agui*2

# Calcular CAS total por mes de C_Responsable de bienestar SRE

for mes in meses_activo12:
    base_intermedia['cas_resp_cont_'+mes] = base_intermedia['C_Responsable de bienestar SRE']*monto_resp

# Calcular aguinaldo total por mes de Coordinadores de Residencia

# Meses con aguinaldo

for mes in meses_agui2:
    base_intermedia['agui_resp_cont_'+mes] = base_intermedia['C_Responsable de bienestar SRE']*monto_agui

# Meses sin aguinaldo

for mes in meses_sinagui2:
    base_intermedia['agui_resp_cont_'+mes] = 0

# 2.2 Responsable de bienestar - 10 meses x 2,500

base_intermedia['cas_resp_nuev_total'] = base_intermedia['Responsable de bienestar SER']*monto_resp*meses_ano10
base_intermedia['agui_resp_nuev_total'] = base_intermedia['Responsable de bienestar SER']*monto_agui*2

for mes in meses_activo10:
    base_intermedia['cas_resp_nuev_'+mes] = base_intermedia['Responsable de bienestar SER']*monto_resp

for mes in meses_inactivo10:
    base_intermedia['cas_resp_nuev_'+mes] = 0

for mes in meses_agui2:
    base_intermedia['agui_resp_nuev_'+mes] = base_intermedia['Responsable de bienestar SER']*monto_agui

for mes in meses_sinagui2:
    base_intermedia['agui_resp_nuev_'+mes] = 0

# 3. Personal de limpieza y mantenimiento - 10 meses

base_intermedia['cas_limp_nuev_total'] = base_intermedia['Limpieza y Mantenimiento']*monto_limp*meses_ano10
base_intermedia['agui_limp_nuev_total'] = base_intermedia['Limpieza y Mantenimiento']*monto_agui*2

for mes in meses_activo10:
    base_intermedia['cas_limp_nuev_'+mes] = base_intermedia['Limpieza y Mantenimiento']*monto_limp

for mes in meses_inactivo10:
    base_intermedia['cas_limp_nuev_'+mes] = 0

for mes in meses_agui2:
    base_intermedia['agui_limp_nuev_'+mes] = base_intermedia['Limpieza y Mantenimiento']*monto_agui

for mes in meses_sinagui2:
    base_intermedia['agui_limp_nuev_'+mes] = 0

# 4. Personal de seguridad nuevos - 10 meses

base_intermedia['cas_segu_nuev_total'] = base_intermedia['Personal de Seguridad']*monto_segu*meses_ano10
base_intermedia['agui_segu_nuev_total'] = base_intermedia['Personal de Seguridad']*monto_agui*2

for mes in meses_activo10:
    base_intermedia['cas_segu_nuev_'+mes] = base_intermedia['Personal de Seguridad']*monto_segu

for mes in meses_inactivo10:
    base_intermedia['cas_segu_nuev_'+mes] = 0

for mes in meses_agui2:
    base_intermedia['agui_segu_nuev_'+mes] = base_intermedia['Personal de Seguridad']*monto_agui

for mes in meses_sinagui2:
    base_intermedia['agui_segu_nuev_'+mes] = 0

# 5.1 Promotores de bienestar continuidad - 12 meses

base_intermedia['cas_prom_cont_total'] = base_intermedia['C_Promotor(a) de bienestar']*monto_prom*meses_ano12
base_intermedia['agui_prom_cont_total'] = base_intermedia['C_Promotor(a) de bienestar']*monto_agui*2

for mes in meses_activo12:
    base_intermedia['cas_prom_cont_'+mes] = base_intermedia['C_Promotor(a) de bienestar']*monto_prom

for mes in meses_agui2:
    base_intermedia['agui_prom_cont_'+mes] = base_intermedia['C_Promotor(a) de bienestar']*monto_agui

for mes in meses_sinagui2:
    base_intermedia['agui_prom_cont_'+mes] = 0

# 5.2 Promotores de bienestar nuevos - 10 meses

base_intermedia['cas_prom_nuev_total'] = base_intermedia['Promotor(a) de bienestar']*monto_prom*meses_ano10
base_intermedia['agui_prom_nuev_total'] = base_intermedia['Promotor(a) de bienestar']*monto_agui*2

for mes in meses_activo10:
    base_intermedia['cas_prom_nuev_'+mes] = base_intermedia['Promotor(a) de bienestar']*monto_prom

for mes in meses_inactivo10:
    base_intermedia['cas_prom_nuev_'+mes] = 0

for mes in meses_agui2:
    base_intermedia['agui_prom_nuev_'+mes] = base_intermedia['Promotor(a) de bienestar']*monto_agui

for mes in meses_sinagui2:
    base_intermedia['agui_prom_nuev_'+mes] = 0

# 6. Personal de cocina nuevos - 10 meses

base_intermedia['cas_coci_nuev_total'] = base_intermedia['Personal de Cocina']*monto_coci*meses_ano10
base_intermedia['agui_coci_nuev_total'] = base_intermedia['Personal de Cocina']*monto_agui*2

for mes in meses_activo10:
    base_intermedia['cas_coci_nuev_'+mes] = base_intermedia['Personal de Cocina']*monto_coci

for mes in meses_inactivo10:
    base_intermedia['cas_coci_nuev_'+mes] = 0

for mes in meses_agui2:
    base_intermedia['agui_coci_nuev_'+mes] = base_intermedia['Personal de Cocina']*monto_agui

for mes in meses_sinagui2:
    base_intermedia['agui_coci_nuev_'+mes] = 0

# 7. Gestores educativos general - 10 meses x 1,400

base_intermedia['cas_gest_g_total'] = base_intermedia['Gestor(a) Educativo(a)']*monto_gest*meses_ano10
base_intermedia['agui_gest_g_total'] = base_intermedia['Gestor(a) Educativo(a)']*monto_agui*2

for mes in meses_activo10:
    base_intermedia['cas_gest_g_'+mes] = base_intermedia['Gestor(a) Educativo(a)']*monto_gest

for mes in meses_inactivo10:
    base_intermedia['cas_gest_g_'+mes] = 0

for mes in meses_agui2:
    base_intermedia['agui_gest_g_'+mes] = base_intermedia['Gestor(a) Educativo(a)']*monto_agui

for mes in meses_sinagui2:
    base_intermedia['agui_gest_g_'+mes] = 0

# 8. Gestores educativos de comunicación - 10 meses x 1,400

base_intermedia['cas_gest_c_total'] = base_intermedia['Gestor(a) Educativo(a) de Comunicación']*monto_gest*meses_ano10
base_intermedia['agui_gest_c_total'] = base_intermedia['Gestor(a) Educativo(a) de Comunicación']*monto_agui*2

for mes in meses_activo10:
    base_intermedia['cas_gest_c_'+mes] = base_intermedia['Gestor(a) Educativo(a) de Comunicación']*monto_gest

for mes in meses_inactivo10:
    base_intermedia['cas_gest_c_'+mes] = 0

for mes in meses_agui2:
    base_intermedia['agui_gest_c_'+mes] = base_intermedia['Gestor(a) Educativo(a) de Comunicación']*monto_agui

for mes in meses_sinagui2:
    base_intermedia['agui_gest_c_'+mes] = 0

# 9. Gestores educativos de matemática - 10 meses x 1,400

base_intermedia['cas_gest_m_total'] = base_intermedia['Gestor(a) Educativo(a) de Matemáticas']*monto_gest*meses_ano10
base_intermedia['agui_gest_m_total'] = base_intermedia['Gestor(a) Educativo(a) de Matemáticas']*monto_agui*2

for mes in meses_activo10:
    base_intermedia['cas_gest_m_'+mes] = base_intermedia['Gestor(a) Educativo(a) de Matemáticas']*monto_gest

for mes in meses_inactivo10:
    base_intermedia['cas_gest_m_'+mes] = 0

for mes in meses_agui2:
    base_intermedia['agui_gest_m_'+mes] = base_intermedia['Gestor(a) Educativo(a) de Matemáticas']*monto_agui

for mes in meses_sinagui2:
    base_intermedia['agui_gest_m_'+mes] = 0

# 10. Gestores educativos de EPT - 10 meses x 1,400

base_intermedia['cas_gest_ept_total'] = base_intermedia['Gestores Educativos EPT cada 120 estud']*monto_gest*meses_ano10
base_intermedia['agui_gest_ept_total'] = base_intermedia['Gestores Educativos EPT cada 120 estud']*monto_agui*2

for mes in meses_activo10:
    base_intermedia['cas_gest_ept_'+mes] = base_intermedia['Gestores Educativos EPT cada 120 estud']*monto_gest

for mes in meses_inactivo10:
    base_intermedia['cas_gest_ept_'+mes] = 0

for mes in meses_agui2:
    base_intermedia['agui_gest_ept_'+mes] = base_intermedia['Gestores Educativos EPT cada 120 estud']*monto_agui

for mes in meses_sinagui2:
    base_intermedia['agui_gest_ept_'+mes] = 0

# b) Cálculo de EsSalud

# Calcular tope de EsSalud

tope_essalud=round(0.09*UIT_porc*UIT_2022)

# Calcular aporte a EsSalud individual, tomar como aporte máximo el valor del tope de EsSalud

base_intermedia['essalud_coor']=min(round(0.09*monto_coor),tope_essalud)
base_intermedia['essalud_gest_g']=min(round(0.09*monto_gest),tope_essalud)
base_intermedia['essalud_gest_c']=min(round(0.09*monto_gest),tope_essalud)
base_intermedia['essalud_gest_m']=min(round(0.09*monto_gest),tope_essalud)
base_intermedia['essalud_gest_ept']=min(round(0.09*monto_gest),tope_essalud)
base_intermedia['essalud_prom']=min(round(0.09*monto_prom),tope_essalud)
base_intermedia['essalud_coci']=min(round(0.09*monto_coci),tope_essalud)
base_intermedia['essalud_segu']=min(round(0.09*monto_segu),tope_essalud)
base_intermedia['essalud_limp']=min(round(0.09*monto_limp),tope_essalud)
base_intermedia['essalud_resp']=min(round(0.09*monto_resp),tope_essalud)

# 1. Coordinadores de residencia - 10 meses

# Calcular aporte a EsSalud total de Coordinadores de Residencia

base_intermedia['essalud_coor_total'] = base_intermedia['Coordinadores de Residencia']*base_intermedia['essalud_coor']*meses_ano10

# Calcular aporte a EsSalud total por mes de Coordinadores de Residencia

# Meses activo

for mes in meses_activo10:
    base_intermedia['essalud_coor_'+mes] = base_intermedia['Coordinadores de Residencia']*base_intermedia['essalud_coor']

# Meses inactivo

for mes in meses_inactivo10:
    base_intermedia['essalud_coor_'+mes] = 0

# 2.1 Responsable de bienestar SRE - 12 meses

# Calcular aporte a EsSalud total de C_Responsable de bienestar SRE

base_intermedia['essalud_resp_cont_total'] = base_intermedia['C_Responsable de bienestar SRE']*base_intermedia['essalud_resp']*meses_ano12

# Calcular aporte a EsSalud total por mes de C_Responsable de bienestar SRE

for mes in meses_activo12:
    base_intermedia['essalud_resp_cont_'+mes] = base_intermedia['C_Responsable de bienestar SRE']*base_intermedia['essalud_resp']

# 2.2 Responsable de bienestar SRE - 10 meses

base_intermedia['essalud_resp_nuev_total'] = base_intermedia['Responsable de bienestar SER']*base_intermedia['essalud_resp']*meses_ano10

for mes in meses_activo10:
    base_intermedia['essalud_resp_nuev_'+mes] = base_intermedia['Responsable de bienestar SER']*base_intermedia['essalud_resp']

for mes in meses_inactivo10:
    base_intermedia['essalud_resp_nuev_'+mes] = 0

# 3. Personal de limpieza y mantenimiento nuevos - 10 meses

base_intermedia['essalud_limp_nuev_total'] = base_intermedia['Limpieza y Mantenimiento']*base_intermedia['essalud_limp']*meses_ano10

for mes in meses_activo10:
    base_intermedia['essalud_limp_nuev_'+mes] = base_intermedia['Limpieza y Mantenimiento']*base_intermedia['essalud_limp']

for mes in meses_inactivo10:
    base_intermedia['essalud_limp_nuev_'+mes] = 0

# 4. Personal de seguridad nuevo - 10 meses

base_intermedia['essalud_segu_nuev_total'] = base_intermedia['Personal de Seguridad']*base_intermedia['essalud_segu']*meses_ano10

for mes in meses_activo10:
    base_intermedia['essalud_segu_nuev_'+mes] = base_intermedia['Personal de Seguridad']*base_intermedia['essalud_segu']

for mes in meses_inactivo10:
    base_intermedia['essalud_segu_nuev_'+mes] = 0

# 5.1 Promotores de bienestar continuidad - 12 meses

base_intermedia['essalud_prom_cont_total'] = base_intermedia['C_Promotor(a) de bienestar']*base_intermedia['essalud_prom']*meses_ano12

for mes in meses_activo12:
    base_intermedia['essalud_prom_cont_'+mes] = base_intermedia['C_Promotor(a) de bienestar']*base_intermedia['essalud_prom']

# 5.2 Promotores de bienestar - nuevo 10 meses

base_intermedia['essalud_prom_nuev_total'] = base_intermedia['Promotor(a) de bienestar']*base_intermedia['essalud_prom']*meses_ano10

for mes in meses_activo10:
    base_intermedia['essalud_prom_nuev_'+mes] = base_intermedia['Promotor(a) de bienestar']*base_intermedia['essalud_prom']

for mes in meses_inactivo10:
    base_intermedia['essalud_prom_nuev_'+mes] = 0

# 6. Personal de cocina - 10 meses

base_intermedia['essalud_coci_nuev_total'] = base_intermedia['Personal de Cocina']*base_intermedia['essalud_coci']*meses_ano10

for mes in meses_activo10:
    base_intermedia['essalud_coci_nuev_'+mes] = base_intermedia['Personal de Cocina']*base_intermedia['essalud_coci']

for mes in meses_inactivo10:
    base_intermedia['essalud_coci_nuev_'+mes] = 0

# 7. Gestores educativos generales - 10 meses

base_intermedia['essalud_gest_g_total'] = base_intermedia['Gestor(a) Educativo(a)']*base_intermedia['essalud_gest_g']*meses_ano10

for mes in meses_activo10:
    base_intermedia['essalud_gest_g_'+mes] = base_intermedia['Gestor(a) Educativo(a)']*base_intermedia['essalud_gest_g']

for mes in meses_inactivo10:
    base_intermedia['essalud_gest_g_'+mes] = 0

# 8. Gestores educativos de comunicación - 10 meses

base_intermedia['essalud_gest_c_total'] = base_intermedia['Gestor(a) Educativo(a) de Comunicación']*base_intermedia['essalud_gest_c']*meses_ano10

for mes in meses_activo10:
    base_intermedia['essalud_gest_c_'+mes] = base_intermedia['Gestor(a) Educativo(a) de Comunicación']*base_intermedia['essalud_gest_c']

for mes in meses_inactivo10:
    base_intermedia['essalud_gest_c_'+mes] = 0

# 9. Gestores educativos de matemática - 10 meses

base_intermedia['essalud_gest_m_total'] = base_intermedia['Gestor(a) Educativo(a) de Matemáticas']*base_intermedia['essalud_gest_m']*meses_ano10

for mes in meses_activo10:
    base_intermedia['essalud_gest_m_'+mes] = base_intermedia['Gestor(a) Educativo(a) de Matemáticas']*base_intermedia['essalud_gest_m']

for mes in meses_inactivo10:
    base_intermedia['essalud_gest_m_'+mes] = 0

# 10. Gestores educativos de EPT - 10 meses

base_intermedia['essalud_gest_ept_total'] = base_intermedia['Gestores Educativos EPT cada 120 estud']*base_intermedia['essalud_gest_ept']*meses_ano10

for mes in meses_activo10:
    base_intermedia['essalud_gest_ept_'+mes] = base_intermedia['Gestores Educativos EPT cada 120 estud']*base_intermedia['essalud_gest_ept']

for mes in meses_inactivo10:
    base_intermedia['essalud_gest_ept_'+mes] = 0

# c) Cálculo de montos totales

# Cálculo de Montos totales por perfil

# 1. Personal de limpieza y mantenimiento nuevos - 10 meses

# Generar variables para totales

base_intermedia['essalud_limp_total']=base_intermedia['essalud_limp_nuev_total']
base_intermedia['cas_limp_total']=base_intermedia['cas_limp_nuev_total']
base_intermedia['agui_limp_total']=base_intermedia['agui_limp_nuev_total']

# Generar variables para totales por mes

for mes in meses_total:
    base_intermedia['cas_limp_'+mes] = base_intermedia['cas_limp_nuev_'+mes]
    base_intermedia['essalud_limp_'+mes] = base_intermedia['essalud_limp_nuev_'+mes]
    base_intermedia['agui_limp_'+mes] = base_intermedia['agui_limp_nuev_'+mes]

# 2. Personal de seguridad nuevos - 10 meses

base_intermedia['essalud_segu_total']=base_intermedia['essalud_segu_nuev_total']
base_intermedia['cas_segu_total']=base_intermedia['cas_segu_nuev_total']
base_intermedia['agui_segu_total']=base_intermedia['agui_segu_nuev_total']

for mes in meses_total:
    base_intermedia['cas_segu_'+mes] = base_intermedia['cas_segu_nuev_'+mes]
    base_intermedia['essalud_segu_'+mes] = base_intermedia['essalud_segu_nuev_'+mes]
    base_intermedia['agui_segu_'+mes] = base_intermedia['agui_segu_nuev_'+mes]

# 3. Promotores de bienestar continuidad y nuevos

# Generar variables para totales: continuidad + nuevos

base_intermedia['essalud_prom_total']=base_intermedia['essalud_prom_cont_total']+base_intermedia['essalud_prom_nuev_total']
base_intermedia['cas_prom_total']=base_intermedia['cas_prom_cont_total']+base_intermedia['cas_prom_nuev_total']
base_intermedia['agui_prom_total']=base_intermedia['agui_prom_cont_total']+base_intermedia['agui_prom_nuev_total']

# Generar variables para totales por mes: continuidad + nuevos

for mes in meses_total:
    base_intermedia['cas_prom_'+mes] = base_intermedia['cas_prom_cont_'+mes]+base_intermedia['cas_prom_nuev_'+mes]
    base_intermedia['essalud_prom_'+mes] = base_intermedia['essalud_prom_cont_'+mes]+base_intermedia['essalud_prom_nuev_'+mes]
    base_intermedia['agui_prom_'+mes] = base_intermedia['agui_prom_cont_'+mes]+base_intermedia['agui_prom_nuev_'+mes]

# 4. Responsable de bienestar SRE continuidad y nuevos

base_intermedia['essalud_resp_total']=base_intermedia['essalud_resp_cont_total']+base_intermedia['essalud_resp_nuev_total']
base_intermedia['cas_resp_total']=base_intermedia['cas_resp_cont_total']+base_intermedia['cas_resp_nuev_total']
base_intermedia['agui_resp_total']=base_intermedia['agui_resp_cont_total']+base_intermedia['agui_resp_nuev_total']

for mes in meses_total:
    base_intermedia['cas_resp_'+mes] = base_intermedia['cas_resp_cont_'+mes]+base_intermedia['cas_resp_nuev_'+mes]
    base_intermedia['essalud_resp_'+mes] = base_intermedia['essalud_resp_cont_'+mes]+base_intermedia['essalud_resp_nuev_'+mes]
    base_intermedia['agui_resp_'+mes] = base_intermedia['agui_resp_cont_'+mes]+base_intermedia['agui_resp_nuev_'+mes]

# 5. Personal de cocina nuevos - 10 meses

base_intermedia['essalud_coci_total']=base_intermedia['essalud_coci_nuev_total']
base_intermedia['cas_coci_total']=base_intermedia['cas_coci_nuev_total']
base_intermedia['agui_coci_total']=base_intermedia['agui_coci_nuev_total']

for mes in meses_total:
    base_intermedia['cas_coci_'+mes] = base_intermedia['cas_coci_nuev_'+mes]
    base_intermedia['essalud_coci_'+mes] = base_intermedia['essalud_coci_nuev_'+mes]
    base_intermedia['agui_coci_'+mes] = base_intermedia['agui_coci_nuev_'+mes]

# Cálculo de Montos Totales

# De Cas

# Monto CAS total de todos los perfiles

base_intermedia['costo_cas_total_anual']=base_intermedia['cas_coci_total']+base_intermedia['cas_coor_total']+base_intermedia['cas_gest_g_total']+base_intermedia['cas_gest_c_total']+base_intermedia['cas_gest_ept_total']+base_intermedia['cas_gest_m_total']+base_intermedia['cas_limp_total']+base_intermedia['cas_prom_total']+base_intermedia['cas_resp_total']+base_intermedia['cas_segu_total']

# Monto CAS total de todos los perfiles por mes

for mes in meses_total:
    base_intermedia['costo_cas_total_'+mes]=base_intermedia['cas_coci_'+mes]+base_intermedia['cas_coor_'+mes]+base_intermedia['cas_gest_g_'+mes]+base_intermedia['cas_gest_c_'+mes]+base_intermedia['cas_gest_ept_'+mes]+base_intermedia['cas_gest_m_'+mes]+base_intermedia['cas_limp_'+mes]+base_intermedia['cas_prom_'+mes]+base_intermedia['cas_resp_'+mes]+base_intermedia['cas_segu_'+mes]

# De EsSalud

# Aporte a EsSalud total de todos los perfiles

base_intermedia['costo_essalud_total_anual']=base_intermedia['essalud_coci_total']+base_intermedia['essalud_coor_total']+base_intermedia['essalud_gest_g_total']+base_intermedia['essalud_gest_c_total']+base_intermedia['essalud_gest_ept_total']+base_intermedia['essalud_gest_m_total']+base_intermedia['essalud_limp_total']+base_intermedia['essalud_prom_total']+base_intermedia['essalud_resp_total']+base_intermedia['essalud_segu_total']

# Aporte a EsSalud total de todos los perfiles por mes

for mes in meses_total:
    base_intermedia['costo_essalud_total_'+mes]=base_intermedia['essalud_coci_'+mes]+base_intermedia['essalud_coor_'+mes]+base_intermedia['essalud_gest_g_'+mes]+base_intermedia['essalud_gest_c_'+mes]+base_intermedia['essalud_gest_ept_'+mes]+base_intermedia['essalud_gest_m_'+mes]+base_intermedia['essalud_limp_'+mes]+base_intermedia['essalud_prom_'+mes]+base_intermedia['essalud_resp_'+mes]+base_intermedia['essalud_segu_'+mes]

# De aguinaldos

# Monto de aguinaldo total de todos los perfiles

base_intermedia['costo_agui_total_anual']=base_intermedia['agui_coci_total']+base_intermedia['agui_coor_total']+base_intermedia['agui_gest_g_total']+base_intermedia['agui_gest_c_total']+base_intermedia['agui_gest_ept_total']+base_intermedia['agui_gest_m_total']+base_intermedia['agui_limp_total']+base_intermedia['agui_prom_total']+base_intermedia['agui_resp_total']+base_intermedia['agui_segu_total']

# Monto de aguinaldo total de todos los perfiles por mes

for mes in meses_total:
    base_intermedia['costo_agui_total_'+mes]=base_intermedia['agui_coci_'+mes]+base_intermedia['agui_coor_'+mes]+base_intermedia['agui_gest_g_'+mes]+base_intermedia['agui_gest_c_'+mes]+base_intermedia['agui_gest_ept_'+mes]+base_intermedia['agui_gest_m_'+mes]+base_intermedia['agui_limp_'+mes]+base_intermedia['agui_prom_'+mes]+base_intermedia['agui_resp_'+mes]+base_intermedia['agui_segu_'+mes]

# Renombrar y generar los perfiles CAS

base_intermedia['n_coci']=base_intermedia['Personal de Cocina']
base_intermedia['n_coor']=base_intermedia['Coordinadores de Residencia']
base_intermedia['n_gest_g']=base_intermedia['Gestor(a) Educativo(a)']
base_intermedia['n_gest_c']=base_intermedia['Gestor(a) Educativo(a) de Comunicación']
base_intermedia['n_gest_ept']=base_intermedia['Gestores Educativos EPT cada 120 estud']
base_intermedia['n_gest_m']=base_intermedia['Gestor(a) Educativo(a) de Matemáticas']
base_intermedia['n_limp']=base_intermedia['Limpieza y Mantenimiento']
base_intermedia['n_prom']=base_intermedia['C_Promotor(a) de bienestar']+base_intermedia['Promotor(a) de bienestar']
base_intermedia['n_resp']=base_intermedia['C_Responsable de bienestar SRE']+base_intermedia['Responsable de bienestar SER']
base_intermedia['n_segu']=base_intermedia['Personal de Seguridad']

# d) Exportar componentes del PxQ

# CAS SRE

# Generar base CAS SRE

cas_sre=base_intermedia[['cod_mod','anexo','cod_local','cod_pliego','nom_pliego','cod_ue','nom_ue','cod_ugel','ugel','cen_edu','n_estu_resi','n_estu_resi_f','n_estu_resi_m','n_coci','n_coor','n_gest_g','n_gest_c','n_gest_ept','n_gest_m','n_limp','n_prom','n_resp','n_segu','costo_cas_total_anual','costo_essalud_total_anual','costo_agui_total_anual','cas_coci_total','cas_coor_total','cas_gest_g_total','cas_gest_c_total','cas_gest_ept_total','cas_gest_m_total','cas_limp_total','cas_prom_total','cas_resp_total','cas_segu_total','essalud_coci_total','essalud_coor_total','essalud_gest_g_total','essalud_gest_c_total','essalud_gest_ept_total','essalud_gest_m_total','essalud_limp_total','essalud_prom_total','essalud_resp_total','essalud_segu_total','agui_coci_total','agui_coor_total','agui_gest_g_total','agui_gest_c_total','agui_gest_ept_total','agui_gest_m_total','agui_limp_total','agui_prom_total','agui_resp_total','agui_segu_total']]

# Exportar CAS SRE

cas_sre.to_excel(ruta_output+'/CAS_SRE_2022_2302.xlsx', sheet_name='internados' , index= False)

# Exportar PxQ DREUGEL

base_intermedia['n_ie']=1

# Agrupar a nivel de cod_pliego, nom_pliego, cod_ue, nom_ue, cod_ugel, ugel (collapse)

pxq_dreugel=base_intermedia.groupby(['cod_pliego','nom_pliego','cod_ue','nom_ue','cod_ugel','ugel'])[['n_ie','n_estudiantes','n_coor','n_gest_g','n_gest_c','n_gest_m','n_gest_ept','n_prom','n_coci','n_limp','n_segu','n_resp','cas_coor_total','essalud_coor_total','agui_coor_total','cas_gest_g_total','essalud_gest_g_total','agui_gest_g_total','cas_gest_c_total','essalud_gest_c_total','agui_gest_c_total','cas_gest_m_total','essalud_gest_m_total','agui_gest_m_total','cas_gest_ept_total','essalud_gest_ept_total','agui_gest_ept_total','cas_prom_total','essalud_prom_total','agui_prom_total','cas_coci_total','essalud_coci_total','agui_coci_total','cas_limp_total','essalud_limp_total','agui_limp_total','cas_segu_total','essalud_segu_total','agui_segu_total','cas_resp_total','essalud_resp_total','agui_resp_total']].sum()

# Exportar

pxq_dreugel.to_excel(ruta_output+'/PxQ_DREUGEL_2302.xlsx', sheet_name='PxQ_DREUGEL' , index= False)

# Exportar PxQ UE

# Agrupar a nivel de cod_pliego, nom_pliego, cod_ue, nom_ue (collapse)

pxq_ue=base_intermedia.groupby(['cod_pliego','nom_pliego','cod_ue','nom_ue'])[['n_ie','n_estudiantes','n_coor','n_gest_g','n_gest_c','n_gest_m','n_gest_ept','n_prom','n_coci','n_limp','n_segu','n_resp','cas_coor_total','essalud_coor_total','agui_coor_total','cas_gest_g_total','essalud_gest_g_total','agui_gest_g_total','cas_gest_c_total','essalud_gest_c_total','agui_gest_c_total','cas_gest_m_total','essalud_gest_m_total','agui_gest_m_total','cas_gest_ept_total','essalud_gest_ept_total','agui_gest_ept_total','cas_prom_total','essalud_prom_total','agui_prom_total','cas_coci_total','essalud_coci_total','agui_coci_total','cas_limp_total','essalud_limp_total','agui_limp_total','cas_segu_total','essalud_segu_total','agui_segu_total','cas_resp_total','essalud_resp_total','agui_resp_total']].sum()

# Exportar

pxq_ue.to_excel(ruta_output+'/PxQ_UE_2302.xlsx', sheet_name='PxQ_UE' , index= False)

# Exportar Metas Físicas - PxQ

sre_mfa=base_intermedia[['cod_pliego','nom_pliego','cod_ue','nom_ue','cod_ugel','ugel','cod_mod','anexo','cod_local','n_estudiantes','n_estu_resi','n_estu_noresi','n_estu_resi_m','n_estu_resi_f','n_coor','n_gest_g','n_gest_c','n_gest_m','n_gest_ept','n_prom','n_coci','n_limp','n_segu','n_resp']]

# Ordenar por cod_pliego y cod_ue

sre_mf=sre_mfa.sort_values(by=['cod_pliego','cod_ue'])

# Exportar

sre_mf.to_excel(ruta_output+'/SRE_2021_metas_fisicas_2302.xlsx', sheet_name='Metas_físicas' , index= False)

'''
        ETAPA 4: Base SIAF (formato MINEDU)

'''

# Generar base a nivel UGEL

b_ugel=base_intermedia.groupby(['cod_pliego','nom_pliego','cod_ue','nom_ue','cod_ugel','ugel'])['costo_cas_total_anual','costo_cas_total_ene','costo_cas_total_feb','costo_cas_total_mar','costo_cas_total_abr','costo_cas_total_may','costo_cas_total_jun','costo_cas_total_jul','costo_cas_total_ago','costo_cas_total_set','costo_cas_total_oct','costo_cas_total_nov','costo_cas_total_dic','costo_essalud_total_anual','costo_essalud_total_ene','costo_essalud_total_feb','costo_essalud_total_mar','costo_essalud_total_abr','costo_essalud_total_may','costo_essalud_total_jun','costo_essalud_total_jul','costo_essalud_total_ago','costo_essalud_total_set','costo_essalud_total_oct','costo_essalud_total_nov','costo_essalud_total_dic','costo_agui_total_anual','costo_agui_total_ene','costo_agui_total_feb','costo_agui_total_mar','costo_agui_total_abr','costo_agui_total_may','costo_agui_total_jun','costo_agui_total_jul','costo_agui_total_ago','costo_agui_total_set','costo_agui_total_oct','costo_agui_total_nov','costo_agui_total_dic'].sum()

# Renombrar variables CAS

b_ugel.rename(columns={'costo_cas_total_anual':'name1_13'},inplace=True)
b_ugel.rename(columns={'costo_cas_total_ene':'name1_1'},inplace=True)
b_ugel.rename(columns={'costo_cas_total_feb':'name1_2'},inplace=True)
b_ugel.rename(columns={'costo_cas_total_mar':'name1_3'},inplace=True)
b_ugel.rename(columns={'costo_cas_total_abr':'name1_4'},inplace=True)
b_ugel.rename(columns={'costo_cas_total_may':'name1_5'},inplace=True)
b_ugel.rename(columns={'costo_cas_total_jun':'name1_6'},inplace=True)
b_ugel.rename(columns={'costo_cas_total_jul':'name1_7'},inplace=True)
b_ugel.rename(columns={'costo_cas_total_ago':'name1_8'},inplace=True)
b_ugel.rename(columns={'costo_cas_total_set':'name1_9'},inplace=True)
b_ugel.rename(columns={'costo_cas_total_oct':'name1_10'},inplace=True)
b_ugel.rename(columns={'costo_cas_total_nov':'name1_11'},inplace=True)
b_ugel.rename(columns={'costo_cas_total_dic':'name1_12'},inplace=True)

# Renombrar variables EsSalud

b_ugel.rename(columns={'costo_essalud_total_anual':'name2_13'},inplace=True)
b_ugel.rename(columns={'costo_essalud_total_ene':'name2_1'},inplace=True)
b_ugel.rename(columns={'costo_essalud_total_feb':'name2_2'},inplace=True)
b_ugel.rename(columns={'costo_essalud_total_mar':'name2_3'},inplace=True)
b_ugel.rename(columns={'costo_essalud_total_abr':'name2_4'},inplace=True)
b_ugel.rename(columns={'costo_essalud_total_may':'name2_5'},inplace=True)
b_ugel.rename(columns={'costo_essalud_total_jun':'name2_6'},inplace=True)
b_ugel.rename(columns={'costo_essalud_total_jul':'name2_7'},inplace=True)
b_ugel.rename(columns={'costo_essalud_total_ago':'name2_8'},inplace=True)
b_ugel.rename(columns={'costo_essalud_total_set':'name2_9'},inplace=True)
b_ugel.rename(columns={'costo_essalud_total_oct':'name2_10'},inplace=True)
b_ugel.rename(columns={'costo_essalud_total_nov':'name2_11'},inplace=True)
b_ugel.rename(columns={'costo_essalud_total_dic':'name2_12'},inplace=True)

# Renombrar variables aguinaldo

b_ugel.rename(columns={'costo_agui_total_anual':'name3_13'},inplace=True)
b_ugel.rename(columns={'costo_agui_total_ene':'name3_1'},inplace=True)
b_ugel.rename(columns={'costo_agui_total_feb':'name3_2'},inplace=True)
b_ugel.rename(columns={'costo_agui_total_mar':'name3_3'},inplace=True)
b_ugel.rename(columns={'costo_agui_total_abr':'name3_4'},inplace=True)
b_ugel.rename(columns={'costo_agui_total_may':'name3_5'},inplace=True)
b_ugel.rename(columns={'costo_agui_total_jun':'name3_6'},inplace=True)
b_ugel.rename(columns={'costo_agui_total_jul':'name3_7'},inplace=True)
b_ugel.rename(columns={'costo_agui_total_ago':'name3_8'},inplace=True)
b_ugel.rename(columns={'costo_agui_total_set':'name3_9'},inplace=True)
b_ugel.rename(columns={'costo_agui_total_oct':'name3_10'},inplace=True)
b_ugel.rename(columns={'costo_agui_total_nov':'name3_11'},inplace=True)
b_ugel.rename(columns={'costo_agui_total_dic':'name3_12'},inplace=True)

# Quitar el índice de la base a nivel UGEL para usar melt (reshape)

b_ugel_ri = b_ugel.reset_index()

# Usar melt para pasar a long (reshape long)

b_ugel_long=pd.melt(b_ugel_ri, id_vars=['cod_pliego', 'cod_ue', 'cod_ugel','nom_pliego','nom_ue','ugel'], value_vars=b_ugel_ri.columns[[x.startswith('name') for x in b_ugel_ri.columns]].tolist(), var_name='s', value_name='name')

# Quitar el índice

b_ugel_long_ri = b_ugel_long.reset_index()

# Extraer dígitos de namex_x antes del subguión y almacenar en la variable valor

b_ugel_long_ri['valor']=b_ugel_long_ri.s.str.extract('(\d+)')

# Extraer dígitos de namex_x después del subguión y almacenar en la variable mes

b_ugel_long_ri['mes']=b_ugel_long_ri['s'].str.extract('(?:.*_)([0-9]+)')

# Eliminar variable s

del b_ugel_long_ri['s']

# Usar pivot para pasar a wide (reshape wide)

b_ugel_wide=b_ugel_long_ri.pivot(index=['cod_pliego', 'cod_ue', 'cod_ugel','valor','nom_pliego','nom_ue','ugel'], columns='mes', values='name')

# Quitar el índice

b_ugel_wide_ri = b_ugel_wide.reset_index()

# Ordenar

b_ugel_f = b_ugel_wide_ri[['cod_pliego', 'cod_ue', 'cod_ugel','valor','nom_pliego','nom_ue','ugel','1','2','3','4','5','6','7','8','9','10','11','12','13']]

# Generar ítems Base SIAF

# Función

b_ugel_f['cod_func']=22
b_ugel_f['funcion']='22. EDUCACION'

# Division funcional: SRE corresponde a una única categoría

b_ugel_f['cod_divfunc']=47
b_ugel_f['division_funcional']='047. EDUCACION BASICA'

# Grupo funcional

b_ugel_f['cod_grupofunc']=105
b_ugel_f['grupo_funcional']='0105. EDUCACION SECUNDARIA'

# Programa presupuestal

b_ugel_f['cod_pp']=150
b_ugel_f['programa_presupuestal']='0150. INCREMENTO EN EL ACCESO DE LA POBLACIÓN A LOS SERVICIOS EDUCATIVOS PÚBLICOS DE LA EDUCACIÓN BASICA'

# Producto

b_ugel_f['cod_prod']=3000868
b_ugel_f['producto_proy']='3000868. MODELOS DE SERVICIOS EDUCATIVOS VALIDADO'

# Actividad

b_ugel_f['cod_act']=5006242
b_ugel_f['actividad_obra']='5006242. IMPLEMENTACION DE PILOTO DE MODELO DE SERVICIO EDUCATIVO'

# Generar correlativo

b_ugel_f.loc[(b_ugel_f['valor']=='1'),'corr'] = '3.2.8.1.1.'
b_ugel_f.loc[(b_ugel_f['valor']=='2'),'corr'] = '3.2.8.1.2.'
b_ugel_f.loc[(b_ugel_f['valor']=='3'),'corr'] = '3.2.8.1.4.'

# Componente: Todo corresponde a Contratación CAS

b_ugel_f['componente']='CONTRATACION CAS'

# Extraer dígitos del correlativo y generar variables

b_ugel_f['cod_gen'] = b_ugel_f['corr'].str[0:1]
b_ugel_f['cod_subgg'] = b_ugel_f['corr'].str[2:3]
b_ugel_f['cod_subgg2'] = b_ugel_f['corr'].str[4:5]
b_ugel_f['cod_espec'] = b_ugel_f['corr'].str[6:7]
b_ugel_f['cod_espec2'] = b_ugel_f['corr'].str[8:9]

# Importar etiquetas

# Importar Base Genérica

b_gen = pd.read_excel(ruta_input+'/base_generica.xlsx',sheet_name='Genericas',header=0,engine='openpyxl')

# Importar Pliego UGEL

pliego_ugel = pd.read_excel(ruta_input+'/base_ue_ugel_ubigeo_2022_v5.xlsx',sheet_name='Sheet1',header=0,engine='openpyxl')

# Renombrar variables

pliego_ugel.rename(columns={'PLIEGO':'cod_pliego'},inplace=True)
pliego_ugel.rename(columns={'EJECUTORA':'cod_ue'},inplace=True)
pliego_ugel.rename(columns={'CODOOII':'codooii'},inplace=True)
pliego_ugel.rename(columns={'NOM_PLIEGO':'nom_pliego'},inplace=True)
pliego_ugel.rename(columns={'NOM_UE':'nom_ue'},inplace=True)

# Eliminar valores nan

pliego_ugel= pliego_ugel.dropna()

# Verificar tipo de variables

print(pliego_ugel.dtypes)

# Cambiar codooii primero a int luego a str

pliego_ugel.codooii=pliego_ugel.codooii.astype(int)

pliego_ugel.codooii=pliego_ugel.codooii.astype(str)

# Agregar 0 a la izquierda

pliego_ugel['codooii']= pliego_ugel['codooii'].str.zfill(6)

# Combinar bases usando inner: Base UGEL final y Base Genérica

ugel_gen=pd.merge(b_ugel_f, b_gen, on ='corr', how ="inner")

# Renombrar variable

ugel_gen.rename(columns={'cod_ugel':'codooii'},inplace=True)

# Combinar bases usando inner: Base UGEL final y Pliego UGEL

ugel_pliegoa=pd.merge(ugel_gen, pliego_ugel, on =['cod_pliego','cod_ue','codooii','nom_pliego','nom_ue'], how ="inner")

# Renombrar variables

ugel_pliegoa.rename(columns={'codooii':'cod_ugel'},inplace=True)

ugel_pliegoa.rename(columns={'13':'costo_anual'},inplace=True)
ugel_pliegoa.rename(columns={'1':'enero'},inplace=True)
ugel_pliegoa.rename(columns={'2':'febrero'},inplace=True)
ugel_pliegoa.rename(columns={'3':'marzo'},inplace=True)
ugel_pliegoa.rename(columns={'4':'abril'},inplace=True)
ugel_pliegoa.rename(columns={'5':'mayo'},inplace=True)
ugel_pliegoa.rename(columns={'6':'junio'},inplace=True)
ugel_pliegoa.rename(columns={'7':'julio'},inplace=True)
ugel_pliegoa.rename(columns={'8':'agosto'},inplace=True)
ugel_pliegoa.rename(columns={'9':'setiembre'},inplace=True)
ugel_pliegoa.rename(columns={'10':'octubre'},inplace=True)
ugel_pliegoa.rename(columns={'11':'noviembre'},inplace=True)
ugel_pliegoa.rename(columns={'12':'diciembre'},inplace=True)

# Ordenar

ugel_pliego=ugel_pliegoa[['nom_pliego','cod_pliego','nom_ue','cod_ue','ugel','cod_ugel','programa_presupuestal','cod_pp','producto_proy','cod_prod','actividad_obra','cod_act','funcion','cod_func','division_funcional','cod_divfunc','grupo_funcional','cod_grupofunc','generica','cod_gen','subgenerica','cod_subgg','subgenerica_det','cod_subgg2','especifica','cod_espec','especifica_det','cod_espec2','componente','corr','correlativo','enero','febrero','marzo','abril','mayo','junio','julio','agosto','setiembre','octubre','noviembre','diciembre','costo_anual']]

# Validar cálculos y exportar

ugel_pliego['anual']=ugel_pliego['enero']+ugel_pliego['febrero']+ugel_pliego['marzo']+ugel_pliego['abril']+ugel_pliego['mayo']+ugel_pliego['junio']+ugel_pliego['julio']+ugel_pliego['agosto']+ugel_pliego['setiembre']+ugel_pliego['octubre']+ugel_pliego['noviembre']+ugel_pliego['diciembre']

# Eliminar variable de validación

del ugel_pliego['anual']

# Eliminar filas donde el costo anual sea 0

ugel_pliego=ugel_pliego[ugel_pliego['costo_anual'] != 0]

# Agrupar a nivel de 'cod_pliego','nom_pliego','cod_ue','nom_ue','cod_ugel','ugel','cod_pp','programa_presupuestal','cod_prod','producto_proy','cod_act','actividad_obra','cod_func','funcion','cod_divfunc','division_funcional','cod_grupofunc','grupo_funcional','cod_gen','generica','cod_subgg','subgenerica','cod_subgg2','subgenerica_det','cod_espec','especifica','cod_espec2','especifica_det','componente','corr','correlativo' (collapse)

sre_siaf=ugel_pliego.groupby(['cod_pliego','nom_pliego','cod_ue','nom_ue','cod_ugel','ugel','cod_pp','programa_presupuestal','cod_prod','producto_proy','cod_act','actividad_obra','cod_func','funcion','cod_divfunc','division_funcional','cod_grupofunc','grupo_funcional','cod_gen','generica','cod_subgg','subgenerica','cod_subgg2','subgenerica_det','cod_espec','especifica','cod_espec2','especifica_det','componente','corr','correlativo'])['enero','febrero','marzo','abril','mayo','junio','julio','agosto','setiembre','octubre','noviembre','diciembre','costo_anual'].sum()

# Quitar el índice

sre_siaf_ri = sre_siaf.reset_index()

# Exportar base SRE SIAF Componente

sre_siaf_ri.to_excel(ruta_output+'/sre_2022_siaf_componente_2302.xlsx', sheet_name='SRE' , index= False)

sre_siaf_ri.to_stata(ruta_output+'/sre_2022_siaf_componente_2302.dta')

'''
        ETAPA 5: Base SIAF (formato MEF)

'''

# Importar base UE UGEL

base_ue_ugel = pd.read_excel(ruta_input+'/base_ue_ugel_ubigeo_2022_v5.xlsx',sheet_name='Sheet1',header=0,engine='openpyxl')

# Eliminar valores nan

base_ue_ugel= base_ue_ugel.dropna()

# Cambiar codooii primero a int luego a str

base_ue_ugel.CODOOII=base_ue_ugel.CODOOII.astype(int)

base_ue_ugel.CODOOII=base_ue_ugel.CODOOII.astype(str)

# Agregar 0 a la izquierda

base_ue_ugel['CODOOII']= base_ue_ugel['CODOOII'].str.zfill(6)

# Renombrar variables

base_ue_ugel.rename(columns={'PLIEGO':'cod_pliego'},inplace=True)
base_ue_ugel.rename(columns={'EJECUTORA':'cod_ue'},inplace=True)
base_ue_ugel.rename(columns={'CODOOII':'cod_ugel'},inplace=True)

# Combinar bases usando inner: Base SRE SIAF Componente y Base UE UGEL

sre_siaf_ue_ugel=pd.merge(sre_siaf_ri, base_ue_ugel, on =['cod_pliego','cod_ue','cod_ugel'], how ="inner")

# Eliminar nombres en formato MINEDU

del sre_siaf_ue_ugel['NOM_PLIEGO']
del sre_siaf_ue_ugel['NOM_UE']
del sre_siaf_ue_ugel['nom_pliego']
del sre_siaf_ue_ugel['nom_ue']
del sre_siaf_ue_ugel['ugel']

# Generar variables

sre_siaf_ue_ugel['ANO_EJE']='2022'
sre_siaf_ue_ugel['SECTOR']='99'
sre_siaf_ue_ugel['NOMBRE_SECTOR']='GOBIERNOS REGIONALE'
sre_siaf_ue_ugel['FUENTE_FINANC']='1'
sre_siaf_ue_ugel['NOMBRE_FUENTE_FINANC']='RECURSOS ORDINARIOS'
sre_siaf_ue_ugel['RUBRO']='00'
sre_siaf_ue_ugel['NOMBRE_RUBRO']='RECURSOS ORDINARIOS'
sre_siaf_ue_ugel['CAT_GASTO']='5'
sre_siaf_ue_ugel['NOMBRE_CAT_GASTO']='GASTOS CORRIENTES'
sre_siaf_ue_ugel['TIPO_TRANSACCION']='2'
sre_siaf_ue_ugel['NOMBRE_TIPO_TRANSACCION']='GASTOS PRESUPUESTARIOS'
sre_siaf_ue_ugel['INTERVENCION']='Secundaria con Residencia Estudiantil'
sre_siaf_ue_ugel['META']='00001'
sre_siaf_ue_ugel['FINALIDAD']='0258420'
sre_siaf_ue_ugel['NOMBRE_FINALIDAD']='IMPLEMENTACION DE PILOTO DE MODELO DE SERVICIO EDUCATIVO PARA EDUCACION SECUNDARIA'
sre_siaf_ue_ugel['UNIDAD_MEDIDA']='201'
sre_siaf_ue_ugel['NOMBRE_UNIDAD_MEDIDA']='INFORME TECNICO'
sre_siaf_ue_ugel['CANTIDAD_META']=1

# Extraer dígitos por código y asignar nombres

sre_siaf_ue_ugel['PROG_PRESUPUESTAL']=sre_siaf_ue_ugel.programa_presupuestal.str.extract('.([^.]+)')
sre_siaf_ue_ugel['NOMBRE_PROG_PRESUPUESTAL'] = sre_siaf_ue_ugel['programa_presupuestal'].str[6:]

sre_siaf_ue_ugel['PRODUCTO_PROYECTO']=sre_siaf_ue_ugel.producto_proy.str.extract('([0-9]+)')
sre_siaf_ue_ugel['NOMBRE_PRODUCTO_PROY'] = sre_siaf_ue_ugel['producto_proy'].str[9:]

sre_siaf_ue_ugel['ACTIVIDAD_OBRA']=sre_siaf_ue_ugel.actividad_obra.str.extract('([0-9]+)')
sre_siaf_ue_ugel['NOMBRE_ACTIVIDAD_NOMBRE'] = sre_siaf_ue_ugel['actividad_obra'].str[9:]

sre_siaf_ue_ugel['FUNCION']=sre_siaf_ue_ugel.funcion.str.extract('([0-9]+)')
sre_siaf_ue_ugel['NOMBRE_FUNCION'] = sre_siaf_ue_ugel['funcion'].str[4:]

sre_siaf_ue_ugel['DIVISION_FUNCIONAL']=sre_siaf_ue_ugel.division_funcional.str.extract('.([^.]+)')
sre_siaf_ue_ugel['NOMBRE_DIVISION_FUNC'] = sre_siaf_ue_ugel['division_funcional'].str[5:]

sre_siaf_ue_ugel['GRUPO_FUNCIONAL']=sre_siaf_ue_ugel.grupo_funcional.str.extract('.([^.]+)')
sre_siaf_ue_ugel['NOMBRE_GRUPO_FUNC'] = sre_siaf_ue_ugel['grupo_funcional'].str[6:]

sre_siaf_ue_ugel['GENERICA']=sre_siaf_ue_ugel.generica.str.extract('([0-9]+)')
sre_siaf_ue_ugel['NOMBRE_GENERICA'] = sre_siaf_ue_ugel['generica'].str[3:]

sre_siaf_ue_ugel['SUB_GENERICA']=sre_siaf_ue_ugel.subgenerica.str.extract('([0-9]+)')
sre_siaf_ue_ugel['NOMBRE_SUB_GENERICA'] = sre_siaf_ue_ugel['subgenerica'].str[3:]

sre_siaf_ue_ugel['SUB_GENERICA_DET']=sre_siaf_ue_ugel.subgenerica_det.str.extract('([0-9]+)')
sre_siaf_ue_ugel['NOMBRE_SUB_GENERICA_DET'] = sre_siaf_ue_ugel['subgenerica_det'].str[3:]

sre_siaf_ue_ugel['ESPECIFICA']=sre_siaf_ue_ugel.especifica.str.extract('([0-9]+)')
sre_siaf_ue_ugel['NOMBRE_ESPECIFICA'] = sre_siaf_ue_ugel['especifica'].str[3:]

sre_siaf_ue_ugel['ESPECIFICA_DET']=sre_siaf_ue_ugel.especifica_det.str.extract('([0-9]+)')
sre_siaf_ue_ugel['NOMBRE_ESPECIFICA_DET'] = sre_siaf_ue_ugel['especifica_det'].str[3:]

# Renombrar variables

sre_siaf_ue_ugel.rename(columns={'cod_pliego':'PLIEGO'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'cod_ue':'EJECUTORA'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'componente':'COMPONENTE'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'enero':'ENERO'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'febrero':'FEBRERO'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'marzo':'MARZO'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'abril':'ABRIL'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'mayo':'MAYO'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'junio':'JUNIO'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'julio':'JULIO'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'agosto':'AGOSTO'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'setiembre':'SEPTIEMBRE'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'octubre':'OCTUBRE'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'noviembre':'NOVIEMBRE'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'diciembre':'DICIEMBRE'},inplace=True)
sre_siaf_ue_ugel.rename(columns={'costo_anual':'MONTO_PROGRAMADO'},inplace=True)

# Agrupar a nivel de componente (collapse)

sre_siaf_mef=sre_siaf_ue_ugel.groupby(['ANO_EJE','SECTOR','NOMBRE_SECTOR','PLIEGO','NOMBRE_PLIEGO','EJECUTORA','NOMBRE_EJECUTORA','PROG_PRESUPUESTAL','NOMBRE_PROG_PRESUPUESTAL','PRODUCTO_PROYECTO','NOMBRE_PRODUCTO_PROY','ACTIVIDAD_OBRA','NOMBRE_ACTIVIDAD_NOMBRE','FUNCION','NOMBRE_FUNCION','DIVISION_FUNCIONAL','NOMBRE_DIVISION_FUNC','GRUPO_FUNCIONAL','NOMBRE_GRUPO_FUNC','META','FINALIDAD','NOMBRE_FINALIDAD','UNIDAD_MEDIDA','NOMBRE_UNIDAD_MEDIDA','CANTIDAD_META','DEPARTAMENTO','NOMBRE_DEPARTAMENTO','PROVINCIA','NOMBRE_PROVINCIA','DISTRITO','NOMBRE_DISTRITO','FUENTE_FINANC','NOMBRE_FUENTE_FINANC','RUBRO','NOMBRE_RUBRO','CAT_GASTO','NOMBRE_CAT_GASTO','TIPO_TRANSACCION','NOMBRE_TIPO_TRANSACCION','GENERICA','NOMBRE_GENERICA','SUB_GENERICA','NOMBRE_SUB_GENERICA','SUB_GENERICA_DET','NOMBRE_SUB_GENERICA_DET','ESPECIFICA','NOMBRE_ESPECIFICA','ESPECIFICA_DET','NOMBRE_ESPECIFICA_DET','INTERVENCION','COMPONENTE'])[['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE','MONTO_PROGRAMADO']].sum()

# Quitar el índice

sre_siaf_mef_ri = sre_siaf_mef.reset_index()

# Exportar base SRE SIAF Componente MEF

#sre_siaf_mef_ri.ANO_EJE=sre_siaf_mef_ri.ANO_EJE.astype(int)
#sre_siaf_mef_ri.SECTOR=sre_siaf_mef_ri.SECTOR.astype(int)

#print(sre_siaf_mef_ri.dtypes)

sre_siaf_mef_ri.to_excel(ruta_output+'/sre_2022_siaf_componente_MEF_2302.xlsx', sheet_name='nombre' , index= False)

sre_siaf_mef_ri.to_stata(ruta_output+'/sre_2022_siaf_componente_MEF_2302.dta')

