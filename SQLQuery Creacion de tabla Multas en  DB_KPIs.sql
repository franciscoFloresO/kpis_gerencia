USE [DB_KPIs];
GO

/*==============================================================*/
/* TABLA: kpi.Multas                                            */
/*==============================================================*/
IF OBJECT_ID(N'[kpi].[Multas]', N'U') IS NOT NULL
    DROP TABLE [kpi].[Multas];
GO

CREATE TABLE [kpi].[Multas]
(
    [id_multa]              INT IDENTITY(1,1) NOT NULL,
    [id_cliente]            INT NOT NULL,
    [id_pais]               INT NOT NULL,
    [fecha_periodo]         DATE NOT NULL,
    [servicio]              NVARCHAR(50) NOT NULL,
    [monto_multa]           DECIMAL(18,2) NOT NULL,
    [descripcion_multa]     NVARCHAR(1000) NULL,
	CONSTRAINT PK_Multas PRIMARY KEY ([id_multa]),
	CONSTRAINT FK_Multas_Cliente FOREIGN KEY (id_cliente)
        REFERENCES cat.Cliente(id_cliente),
    CONSTRAINT FK_Multas_Pais FOREIGN KEY (id_pais)
        REFERENCES cat.Pais(id_pais),
	CONSTRAINT CK_Multas_Servicio
        CHECK ([servicio] IN ('Field Service', 'Service Desk')),
	CONSTRAINT CK_Multas_Fecha
        CHECK (DATEPART(DAY, fecha_periodo) = 1)
);
GO