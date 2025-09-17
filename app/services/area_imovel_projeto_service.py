from repositories.area_imovel_projeto_repository import list_properties

async def list_properties_service(cod_cpf: str):
    return await list_properties(cod_cpf)

