const { Telegraf } = require('telegraf');
const fs = require('fs');
const path = require('path');

// Substitua 'SEU_TOKEN_AQUI' pelo token do seu bot fornecido pelo BotFather
const BOT_TOKEN = '7220758959:AAGvfskMa0Y9yOlczyHdk0IncwG-_DTt8_A';
if (!BOT_TOKEN) {
  process.exit(1);
}

const bot = new Telegraf(BOT_TOKEN);

// Caminho do arquivo para salvar os gastos
const expensesFilePath = path.join(__dirname, 'expenses.json');
let expenses = [];

// Carrega as despesas existentes, se houver
if (fs.existsSync(expensesFilePath)) {
  try {
    const data = fs.readFileSync(expensesFilePath, 'utf8');
    expenses = JSON.parse(data);
  } catch (error) {
    console.error('Erro ao ler o arquivo expenses.json:', error);
  }
}

// Função para salvar os gastos no arquivo JSON
function saveExpenses() {
  try {
    fs.writeFileSync(expensesFilePath, JSON.stringify(expenses, null, 2));
  } catch (error) {
    console.error('Erro ao salvar o arquivo expenses.json:', error);
  }
}

// Comando /start - mensagem inicial
bot.start((ctx) => {
  ctx.reply(
    'Olá, ${ctx.from.first_name}! Sou seu bot de controle de gastos.\n' +
    'Comandos disponíveis:\n' +
    '/add <valor> <descrição> - Adicionar um gasto\n' +
    '/list - Listar todos os gastos\n' +
    '/total - Ver o total gasto\n' +
    '/help - Exibir esta mensagem novamente'
  );
});

// Comando /help - exibe os comandos disponíveis
bot.help((ctx) => {
  ctx.reply(
    'Comandos ,disponíveis,n' +
    '/add <valor> <descrição> - Adicionar um gasto\n' +
    '/list - Listar todos os gastos\n' +
    '/total - Ver o total gasto'
  );
});

// Comando /add - adiciona um gasto
// Exemplo de uso: /add 50 Mercado
bot.command('add', (ctx) => {
  const text = ctx.message.text;
  // Remove o comando "/add" e separa os argumentos
  const args = text.split(' ').slice(1);

  if (args.length < 2) {
    return ctx.reply('Formato incorreto. Use: /add <valor> <descrição>');
  }

  const value = parseFloat(args[0]);
  if (isNaN(value)) {
    return ctx.reply('Valor inválido. Por favor, insira um número válido.');
  }

  const description = args.slice(1).join(' ');
  const expense = {
    value,
    description,
    date: new Date().toISOString()
  };

  expenses.push(expense);
  saveExpenses();

  ctx.reply('Gasto de R$${value,toFixed(2)} ,adicionado, $,{description}');
});

// Comando /list - lista todos os gastos registrados
bot.command('list', (ctx) => {
  if (expenses.length === 0) {
    return ctx.reply('Nenhum gasto registrado.');
  }

  let message = 'Lista de gastos:\n';
  expenses.forEach((expense, index) => {
    message += '${index + 1}. R$${expense,value, toFixed(2)} - $,{expense,description}\n';
  });

  ctx.reply(message);
});

// Comando /total - exibe o total dos gastos
bot.command('total', (ctx) => {
  if (expenses.length === 0) {
    return ctx.reply('Nenhum gasto registrado.');
  }
  const total = expenses.reduce((acc, curr) => acc + curr.value, 0);
  ctx.reply('Total de gasto R$${total,toFixed(2)}');
});

// Inicializa o bot
bot.launch()
  .then(() => console.log('Bot iniciado com sucesso!'))
  .catch((error) => console.error('Erro ao iniciar o bot:', error));