$baseUrl = "https://semana-6.onrender.com/api/gastos/"

Write-Host "`n=== 1. TESTANDO CRIAÃ‡ÃƒO DE REGISTROS (POST) ===" -ForegroundColor Cyan
$cenarios = @(
    @{ descricao = "Teclado Mecanico RGB"; valor = 280.00; categoria = "eletronicos"; impulso = $true },
    @{ descricao = "Mensalidade Curso"; valor = 150.00; categoria = "educacao"; impulso = $false },
    @{ descricao = "Lanche de Sexta"; valor = 35.50; categoria = "outros"; impulso = $true }
)

foreach ($item in $cenarios) {
    $jsonBody = $item | ConvertTo-Json
    $resposta = Invoke-RestMethod -Uri $baseUrl -Method Post -ContentType "application/json" -Body $jsonBody
    Write-Host "[SUCCESS] Registro criado: '$($item.descricao)' | ID Retornado: $($resposta.id)" -ForegroundColor Green
}

Write-Host "`n=== 2. CONSULTANDO O BANCO DE DADOS (GET) ===" -ForegroundColor Cyan
$todosGastos = Invoke-RestMethod -Uri $baseUrl -Method Get
Write-Host "Total de registros cadastrados na nuvem: $($todosGastos.Count)" -ForegroundColor Yellow

Write-Host "`n=== 3. ÃšLTIMOS 3 REGISTROS INSERIDOS ===" -ForegroundColor Cyan
$todosGastos[-3..-1] | Format-Table -AutoSize
