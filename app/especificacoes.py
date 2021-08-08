def get_especificacoes(resultado, tipo):
    especificacoes = {
        'Marca:': resultado.marca,
        'Modelo:' : resultado.modelo,
        'Garantia:': resultado.garantia
    }
    if tipo == 'processadores':
        especificacoes.update({
            'Núcleos:' : resultado.nucleos,
            'Threads:' : resultado.threads,
            'Frequência base:' : resultado.frequencia_base,
            'Frequência turbo:': resultado.frequencia_turbo,
            'TDP:' : resultado.tdp,
            'Soquete:' : resultado.soquete,
            'Litografia:' : resultado.litografia,
            'Tecnologias:' : resultado.tecnologias,
            'Vídeo integrado:' : resultado.video
        })
    elif tipo == 'hds':
        especificacoes.update({
            'Capacidade:' : f'{resultado.capacidade / 1024} TB',
            'Interface:' : resultado.interface,
            'RPM:' : resultado.rpm,
            'Formato:' : f'{resultado.formato / 10}"',
            'Cache:' : f'{resultado.cache} MB'
        })
    return especificacoes
