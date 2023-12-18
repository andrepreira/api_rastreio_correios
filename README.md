## Rastreio Correios API Scraper

https://rastreamento.correios.com.br/app/index.php

Criar uma API que: 
    - recebe o codigo_rastreio de um objeto
    - resolve o captcha
    - passa o payload preenchido
    
    ````python
        payload = {
            "objeto": f"{code}",
            "captcha": f"{captcha}",
            "mqs": "S"
            } 
    ````
    - criar a api com fastapi
    - retorna um json com o handle do HTML

    ````html
        <div id="tabs-rastreamento">
				
			
        <div id="cabecalho-rastro">
            <ul class="cabecalho-rastro">
                <div class="arrow-dashed">
                <div class="circle">
                <img class="circle-img" src="./Rastreamento_files/correios-sf.png" width="35px" height="35px">
                </div>
                </div>
                <div class="cabecalho-content"><p class="text text-head">Previsão de Entrega: 13/12/2023</p>
                    <p class="text text-content">ENCOMENDA PAC</p>
                </div>
            </ul>
        </div>
    
			
        <ul class="ship-steps">
            <li class="step">
        
        <div class="arrow-current">
            <div class="circle">
            <img class="circle-img" src="./Rastreamento_files/caminhao-cor.png">            
            </div>
        </div>
    
        
        <div class="step-content">
            <p class="text text-head">Objeto em trânsito - por favor aguarde</p>
            <p class="text text-content">de Unidade de Tratamento, CAJAMAR - SP</p><p class="text text-content">para Unidade de Tratamento, RECIFE - PE</p>
            
            <p class="text text-content">05/12/2023 05:53</p>
        </div>
    
    </li><li class="step">
        
        <div class="arrow-current">
            <div class="circle">
            <img class="circle-img" src="./Rastreamento_files/caminhao-cor.png">            
            </div>
        </div>
    
        
        <div class="step-content">
            <p class="text text-head">Objeto em trânsito - por favor aguarde</p>
            <p class="text text-content">de Agência dos Correios, ITAPECERICA DA SERRA - SP</p><p class="text text-content">para Unidade de Tratamento, CAJAMAR - SP</p>
            
            <p class="text text-content">29/11/2023 15:23</p>
        </div>
    
    </li><li class="step">
        
        <div class="arrow-none">
            <div class="circle">
            <img class="circle-img" src="./Rastreamento_files/agencia-cor.png">            
            </div>
        </div>
    
        
        <div class="step-content">
            <p class="text text-head">Objeto postado</p>
            <p class="text text-content">ITAPECERICA DA SERRA - SP</p>
            
            <p class="text text-content">29/11/2023 14:22</p>
        </div>
    
    </li>
        </ul>
    
		
				
				
				<a class="btn btn-outline-primary p-1 btn-rastro" href="https://rastreamento.correios.com.br/app/suspensaoEntrega/index.php?objeto=QP487749745BR">
                      <i class="fa fa-hand-paper-o" aria-hidden="true"></i>
                      Suspender Entrega
                </a>
				
	</div>
    
    ````