import requests as req

class TestMovimentacao:
    headers = {'Authorization': 'Token 086eed31c3d817264d4ea2034b698be70a97a40c'}
    url_movimentacao = 'http://127.0.0.1:8000/api/v1/movimentacao/'

    #testes sem usuário logado
    def test_get_movimentacao(self):
        resposta = req.get(url=self.url_movimentacao)
        assert resposta.status_code == 200 and len(resposta.text) == 2 #o tamanho da resposta é 2, caso não recupere nenhum nado
    
    def test_put_movimentacao(self):
        nova_movimentacao = {
            "ativo": 1,
            "quantidade": 5,
            "acao": 1
        }
        resposta = req.put(url=self.url_movimentacao, data=nova_movimentacao)
        assert resposta.status_code == 401 or  resposta.status_code == 403 #sem usuário fornecido
    
    def test_delete_movimentacao(self):
        resposta = req.delete(url=f'{self.url_movimentacao}')

        assert resposta.status_code == 401 or resposta.status_code == 403 
    
    def test_post_movimentacao_logado(self):
        nova_movimentacao = {
            "ativo": 1,
            "quantidade": 5,
            "acao": 1
        }
        resposta = req.post(url=self.url_movimentacao, data=nova_movimentacao)
        resposta = req.delete(url=f'{self.url_movimentacao}', headers=self.headers)

        assert resposta.status_code == 405
    
    #testes com usuário logado
    def test_get_movimentacao_logado(self):
        resposta = req.get(url=self.url_movimentacao, headers=self.headers)
        assert resposta.status_code == 200 and len(resposta.text) > 2
    
    def test_put_movimentacao_logado(self):
        nova_movimentacao = {
            "ativo": 1,
            "quantidade": 5,
            "acao": 1
        }
        resposta = req.put(url=self.url_movimentacao, data=nova_movimentacao, headers=self.headers)
        assert resposta.status_code == 405
    
    def test_delete_movimentacao_logado(self):
        resposta = req.delete(url=f'{self.url_movimentacao}', headers=self.headers)

        assert resposta.status_code == 405
    
    def test_post_movimentacao_logado_aplicacao(self):
        nova_movimentacao = {
            "ativo": 1,
            "quantidade": 5,
            "acao": 1
        }
        resposta = req.post(url=self.url_movimentacao, data=nova_movimentacao, headers=self.headers)
        print(resposta.text)
        assert resposta.status_code == 201
    
    def test_post_movimentacao_logado_retirada(self):
        nova_movimentacao = {
            "ativo": 1,
            "quantidade": 5,
            "acao": 2
        }
        resposta = req.post(url=self.url_movimentacao, data=nova_movimentacao, headers=self.headers)
        print(resposta.text)
        assert resposta.status_code == 201