<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
  
<img src="https://img.freepik.com/free-vector/isometric-composition-with-different-telecommunication-devices-television-equipment-3d-vector-illustration_1284-30577.jpg?w=1380&t=st=1683896149~exp=1683896749~hmac=d9f09c4467a3f80f793870b0c1faf5ca52e3a77facdf27703ebef4fd21771c83" width="100%" height="400px">


<p dir="auto">
<a target="_blank" rel="noopener noreferrer nofollow"><img src="https://camo.githubusercontent.com/f59112f72a9ec9f72a6c124b4ac432217b85524b969f013108b9ec97dbb2a86e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f547970652532306f662532304d4c2d42696e617279253230436c617373696669636174696f6e2d726564" alt="Type of ML" data-canonical-src="https://img.shields.io/badge/Type%20of%20ML-Binary%20Classification-red" style="max-width: 100%;"></a>
  <a href="https://colab.research.google.com/drive/1aLf4ht-arQxBk1YBP2m5FJx4Nr-3Q92i?usp=sharing" rel="nofollow"><img src="https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667" alt="Open In Colab" data-canonical-src="https://colab.research.google.com/assets/colab-badge.svg" style="max-width: 100%;"></a>
  
<h2>TELECOM CHURN PREDICTION</h2>
  
<h2>Authors</h2>
<a href="https://github.com/natalia-gcvs">@natalia-gcvs</a>
  
<h2>Metodologia</h2>
  
  A metodologia utilizada nesse projeto é o CRISP-DM que involve as etapas ilustradas abaixo.

  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/CRISP-DM_Process_Diagram.png/319px-CRISP-DM_Process_Diagram.png">
  
  <ol dir="auto">
<li><a href="#business-problem">Entendimento do negócio</a></li>
<li><a href="#data-source">Entendimento dos dados</a></li>
<li><a href="#methods">Preparação dos dados</a></li>
<li><a href="#tech-stack">Modelagem</a></li>
<li><a href="#quick-glance-at-the-results">Avaliação do modelo</a></li>
<li><a href="#lessons-learned-and-recommendation">Implantação/Deployment</a></li>
<li><a href="#limitation-and-what-can-be-improved">Limitações e pontos a serem melhorados</a></li>
  </ol>
  
<h2>1. Entendimento do Negócio</h2> 
  <ul>
    <li><p><b>Objetivo do projeto:</b> Entender claramente o objetivo do projeto, que neste caso é identificar antecipadamente os clientes com maior probabilidade de cancelar os serviços da empresa de telecomunicações (churn), a fim de tomar medidas proativas para mantê-los satisfeitos e evitar perdas de negócios.</p></li>
    <li><p><b>Contexto do negócio:</b> Compreender o contexto em que o projeto está inserido, incluindo a situação competitiva do mercado, os tipos de serviços oferecidos, as políticas de preços, os canais de atendimento e a percepção dos clientes sobre a empresa. 
<em>No entanto, uma das limitações deste projeto é que a fonte de dados disponível é o Kaggle e a empresa é anônima, o que restringe nossa capacidade de aprofundar a análise do contexto de negócios.</em></p></li>
    <li><p><b>Fontes de dados:</b> Identificar as fontes de dados disponíveis para o projeto, que podem incluir dados de faturamento, perfil dos clientes, histórico de uso dos serviços, informações sobre reclamações e cancelamentos de serviço, entre outros. Asim como na etapa anterior estamos limitadas as variáveis contidas no dataset, cuja fonte é o Kaggle</p></li>
    <li><p><b>Variáveis de interesse:</b> Selecionar as variáveis mais relevantes para o problema de churn, como por exemplo, tempo de contrato, valor do faturamento, tipo de serviço contratado, frequência de uso, histórico de cancelamento, entre outros.</p></li>
    <li><p><b>Stakeholders:</b> Identificar as partes interessadas no projeto, incluindo a equipe de marketing, a equipe de atendimento ao cliente, a equipe de vendas e os próprios clientes, a fim de entender como os resultados do projeto podem impactar esses stakeholders. Essa etapa também não é possível de ser realizada dada a fonte de dados</p></li>
    <li><p><b>Métricas de sucesso:</b> Definir as métricas de sucesso para o projeto. Para lidar com dados desbalanceados, que é o caso, é importante escolher uma métrica de sucesso adequada que leve em consideração a classe minoritária, como a recall e a precision. Como nosso objetivo é identificar corretamente todos os casos de churn, mesmo que isso resulte em alguns falsos positivos, a recall é a métrica mais importante. Isso ocorre porque é mais prejudicial perder um cliente do que investir em um que não deixaria a empresa. No entanto, é importante lembrar que essa decisão depende do contexto do negócio e da capacidade financeira da empresa para lidar com os investimentos necessários.</p></li>
  </ul>
  
  <h2>2. Entendimento dos dados</h2>
  
  <dl>
    <dt>2.1. Coleta de dados:</dt>
    <dd><b>Objetivo:</b> Identificar as fontes de dados relevantes para o projeto e coletar os dados necessários.
      <dd>Essa etapa se resume ao download do dataset no 
      <a href="https://www.kaggle.com/datasets/arashnic/telecom-churn-dataset">Kaggle</a></dd>
 
  
<dt>2.2. Descrição dos dados:</dt>
<dd><b>Objetivo:</b> Descrever os dados para entender melhor suas características, como tamanho, tipo de dados, distribuição, presença de missing values ou outliers.</dd>
<dd>O dataset possui 4250 entradas, das quais:</dd>
<dd>- Somente 14% dos dados representam a classe de clientes que cancelaram o serviço.</dd>
<dd>- O dataset não possui missing values.</dd>
<dd>- Para lidar com outliers, utilizamos uma técnica de imputação, uma vez que eles eram poucos. Não poderíamos simplesmente excluí-los, já que estamos trabalhando com um dataset pequeno e não queremos perder informações relevantes. Além disso, verificamos que as entradas com outliers são válidas. Utilizamos a técnica de Winsorization para lidar com esses outliers, que consiste em recortar os valores discrepantes para os percentis mínimo e máximo.</dd>

  


<dt>2.5. Análise exploratória:</dt> 
    <dd><b>Objetivo:</b>Realizar uma análise exploratória dos dados para entender melhor a estrutura dos dados e como as variáveis estão relacionadas.</dd>

<dt>2.6. Seleção de variáveis:</dt> 
  <dd>Selecionar as variáveis mais relevantes para o problema de churn, levando em consideração a correlação com a variável de interesse, a redundância entre as variáveis e a facilidade de obtenção dos dados.</dd>

<dt>2.7. Identificação de dados sensíveis:</dt> 
  <dd>Identificar se existem dados sensíveis que precisam ser tratados de forma especial para garantir a privacidade e a segurança dos clientes. Não é uma questão relevante para esse projeto.</dd>

<dt>2.8. Preparação dos dados:</dt>
  <dd>Preparar os dados para a próxima etapa, que envolve a construção dos modelos de predição de churn. Isso pode incluir a normalização dos dados, a transformação de variáveis, a criação de variáveis derivadas e a divisão dos dados em conjuntos de treinamento e teste.</dd>

      
  </dl>

 

  
 



</body>
</html>





