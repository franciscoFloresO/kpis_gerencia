USE [DB_KPIs];
GO

/*==============================================================*/
/* TABLA: kpi.ContractualMensualFS                              */
/*==============================================================*/
IF OBJECT_ID(N'[kpi].[ContractualMensualFS]', N'U') IS NOT NULL
    DROP TABLE [kpi].[ContractualMensualFS];
GO

CREATE TABLE [kpi].[ContractualMensualFS]
(
    [id_contractual_mensual]     BIGINT IDENTITY(1,1) NOT NULL,
    [id_cliente]                 INT NOT NULL,
    [id_pais]                    INT NOT NULL,
    [fecha_periodo]              DATE NOT NULL,
    [fecha_contrato_modificacion] DATE NOT NULL,
    [descripcion_servicio]       NVARCHAR(1000) NOT NULL,
    [cobertura_horaria_multas]   NVARCHAR(1000) NOT NULL,
    [epa_objetivo]               DECIMAL(10,4) NULL,
    [fcr_objetivo]               DECIMAL(10,4) NULL,
    [sla_objetivo]               DECIMAL(10,4) NOT NULL,
    [abandono_objetivo]          DECIMAL(10,4) NOT NULL,
    [asa_segundos_objetivo]      INT NOT NULL,
    [tmo_segundos_objetivo]      DECIMAL(10,2) NOT NULL,
    [acw_segundos_objetivo]      INT NULL,
    [agentes_objetivo]           INT NULL,
    [supervisores_objetivo]      INT NULL,
    [backoffice_objetivo]        INT NULL,
    [creado_por]                 INT NOT NULL,
    [fecha_creacion]             DATETIME2(0) NOT NULL
        CONSTRAINT [DF_ContractualMensualFS_fecha_creacion] DEFAULT (SYSDATETIME()),
    [modificado_por]             INT NULL,
    [fecha_modificacion]         DATETIME2(0) NULL,
    CONSTRAINT [PK_ContractualMensualFS]
        PRIMARY KEY CLUSTERED ([id_contractual_mensual] ASC)
);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [UQ_ContractualMensualFS]
UNIQUE NONCLUSTERED
(
    [id_cliente],
    [id_pais],
    [fecha_periodo]
);
GO

CREATE NONCLUSTERED INDEX [IX_ContractualMensualFS_ClientePaisPeriodo]
ON [kpi].[ContractualMensualFS]
(
    [id_cliente],
    [id_pais],
    [fecha_periodo]
);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [FK_ContractualMensualFS_Cliente]
FOREIGN KEY ([id_cliente]) REFERENCES [cat].[Cliente]([id_cliente]);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [FK_ContractualMensualFS_Pais]
FOREIGN KEY ([id_pais]) REFERENCES [cat].[Pais]([id_pais]);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [FK_ContractualMensualFS_CreadoPor]
FOREIGN KEY ([creado_por]) REFERENCES [seg].[UsuarioApp]([id_usuario]);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [FK_ContractualMensualFS_ModificadoPor]
FOREIGN KEY ([modificado_por]) REFERENCES [seg].[UsuarioApp]([id_usuario]);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [CK_CMFS_Abandono]
CHECK ([abandono_objetivo] >= 0 AND [abandono_objetivo] <= 100);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [CK_CMFS_ACW]
CHECK ([acw_segundos_objetivo] IS NULL OR [acw_segundos_objetivo] >= 0);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [CK_CMFS_Agentes]
CHECK ([agentes_objetivo] IS NULL OR [agentes_objetivo] >= 0);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [CK_CMFS_ASA]
CHECK ([asa_segundos_objetivo] >= 0);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [CK_CMFS_Backoffice]
CHECK ([backoffice_objetivo] IS NULL OR [backoffice_objetivo] >= 0);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [CK_CMFS_EPA]
CHECK ([epa_objetivo] >= 0 AND [epa_objetivo] <= 100);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [CK_CMFS_FCR]
CHECK ([fcr_objetivo] >= 0 AND [fcr_objetivo] <= 100);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [CK_CMFS_FechaPeriodo_PrimerDiaMes]
CHECK (DATEPART(DAY, [fecha_periodo]) = 1);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [CK_CMFS_SLA]
CHECK ([sla_objetivo] >= 0 AND [sla_objetivo] <= 100);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [CK_CMFS_Supervisores]
CHECK ([supervisores_objetivo] IS NULL OR [supervisores_objetivo] >= 0);
GO

ALTER TABLE [kpi].[ContractualMensualFS]
ADD CONSTRAINT [CK_CMFS_TMO]
CHECK ([tmo_segundos_objetivo] >= 0);
GO


/*==============================================================*/
/* TABLA: kpi.OperacionMensualFS                                */
/*==============================================================*/
IF OBJECT_ID(N'[kpi].[OperacionMensualFS]', N'U') IS NOT NULL
    DROP TABLE [kpi].[OperacionMensualFS];
GO

CREATE TABLE [kpi].[OperacionMensualFS]
(
    [id_operacion_mensual]       BIGINT IDENTITY(1,1) NOT NULL,
    [id_cliente]                 INT NOT NULL,
    [id_pais]                    INT NOT NULL,
    [fecha_periodo]              DATE NOT NULL,
    [agentes_promedio]           INT NOT NULL,
    [supervisores_promedio]      INT NOT NULL,
    [backoffice_promedio]        INT NOT NULL,
    [tickets_humano]             INT NOT NULL,
    [hibridos_whatsapp_bi]       INT NOT NULL,
    [porcentaje_digitalizacion]  INT NOT NULL,
    [ingresos_totales_usd]       DECIMAL(18,2) NOT NULL,
    [costos_totales_usd]         DECIMAL(18,2) NULL,
    [costo_ticket_usd]           DECIMAL(18,4) NULL,
    [codigo_moneda]              CHAR(3) NOT NULL
        CONSTRAINT [DF_OperacionMensualFS_moneda] DEFAULT ('USD'),
    [creado_por]                 INT NOT NULL,
    [fecha_creacion]             DATETIME2(0) NOT NULL
        CONSTRAINT [DF_OperacionMensualFS_fecha_creacion] DEFAULT (SYSDATETIME()),
    [modificado_por]             INT NULL,
    [fecha_modificacion]         DATETIME2(0) NULL,
    [tickets_digital]            INT NULL,
    CONSTRAINT [PK_OperacionMensualFS]
        PRIMARY KEY CLUSTERED ([id_operacion_mensual] ASC)
);
GO

ALTER TABLE [kpi].[OperacionMensualFS]
ADD CONSTRAINT [UQ_OperacionMensualFS]
UNIQUE NONCLUSTERED
(
    [id_cliente],
    [id_pais],
    [fecha_periodo]
);
GO

CREATE NONCLUSTERED INDEX [IX_OperacionMensualFS_ClientePaisPeriodo]
ON [kpi].[OperacionMensualFS]
(
    [id_cliente],
    [id_pais],
    [fecha_periodo]
);
GO

ALTER TABLE [kpi].[OperacionMensualFS]
ADD CONSTRAINT [FK_OperacionMensualFS_Cliente]
FOREIGN KEY ([id_cliente]) REFERENCES [cat].[Cliente]([id_cliente]);
GO

ALTER TABLE [kpi].[OperacionMensualFS]
ADD CONSTRAINT [FK_OperacionMensualFS_Pais]
FOREIGN KEY ([id_pais]) REFERENCES [cat].[Pais]([id_pais]);
GO

ALTER TABLE [kpi].[OperacionMensualFS]
ADD CONSTRAINT [FK_OperacionMensualFS_CreadoPor]
FOREIGN KEY ([creado_por]) REFERENCES [seg].[UsuarioApp]([id_usuario]);
GO

ALTER TABLE [kpi].[OperacionMensualFS]
ADD CONSTRAINT [FK_OperacionMensualFS_ModificadoPor]
FOREIGN KEY ([modificado_por]) REFERENCES [seg].[UsuarioApp]([id_usuario]);
GO

ALTER TABLE [kpi].[OperacionMensualFS]
ADD CONSTRAINT [CK_OperacionMensualFS_CodigoMoneda]
CHECK ([codigo_moneda] = 'USD');
GO

ALTER TABLE [kpi].[OperacionMensualFS]
ADD CONSTRAINT [CK_OperacionMensualFS_FechaPeriodo_PrimerDiaMes]
CHECK (DATEPART(DAY, [fecha_periodo]) = 1);
GO