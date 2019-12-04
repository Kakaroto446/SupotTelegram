# -*- coding: utf-8 -*-
# File: core.py
# Created by: Johnny Barbosa
# Date: 07/11/2019
# Description: Main archive of the bot, contain all steps of the conversation

import logging
import postman
from credentials import *
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

#config log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

#Definiçao dos estados de relatar problema
RELATAR_PROBLEMA, COOP, AREA, DESCRICAO, ANEXO, FREQUENCIA = range(6)

# Shortcut for ConversationHandler.END
END = ConversationHandler.END

#função para quando derem um /start
def start(update, context):
    reply_keyboard = [['Relatar problema', 'Obter ajuda']]

    update.message.reply_text(
        "Olá, sou o bot de suporte da technoplus"
        "\nNo que posso ajudar?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return RELATAR_PROBLEMA

def relatar_problema(update, context):
    cod = 0
    user = update.message.from_user    
    update.message.reply_text("Me diga, qual o nome da sua cooperativa?", reply_markup=ReplyKeyboardRemove())
    postman.env_relatorio(cod, user.first_name)
    
    return COOP
    
def cooperativa(update, context):
    cod = 1
    coop = update.message.text
    postman.env_relatorio(cod, coop)
    text = 'Anotado, agora me diga, qual a área do problema?'
    reply_keyboard = [['Cadastro', 'Escala'],['Produtividade', 'Processos'],['Relatórios', 'Acesso']]
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return AREA    
    
def area(update, context):
    cod = 2
    area = update.message.text
    postman.env_relatorio(cod, area)
    texto = "Okay, agora digite na próxima mensagem uma breve descrição do que aconteceu"
    update.message.reply_text(texto, reply_markup=ReplyKeyboardRemove())
   
    return DESCRICAO

def descricao(update, context):
    cod = 3
    desc = update.message.text
    postman.env_relatorio(cod, desc)
    update.message.reply_text("Ótimo, isso já vai nos ajudar bastante! Se quiser anexar algum arquivo, mande-o agora. Caso contrário digite /skip")
    
    return ANEXO

def anexo(update, context):
    cod = 5
    user = update.message.from_user
    anexo = update.message.photo[-1].get_file()
    anexo.download('user_photo.jpg')
    reply_keyboard = [['Sempre', 'Às vezes'], ['Aleatório', 'Não se tentou'], ['Incapaz de reproduzir', 'ND']]  
    update.message.reply_text("Ótimo! Só mais uma coisinha, com que frequência isso ocorre?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return FREQUENCIA
    
def skip_anexo(update, context): 
    cod = 4
    texto = "null"
    postman.env_relatorio(cod, texto)
    reply_keyboard = [['Sempre', 'Às vezes'], ['Aleatório', 'Não se tentou'], ['Incapaz de reproduzir', 'ND']]  
    update.message.reply_text("Ótimo! Só mais uma coisinha, com que frequência isso ocorre?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return FREQUENCIA
    
def freq(update, context):
    cod = 6
    freq = update.message.text
    postman.env_relatorio(cod, freq)
    #parei aqui

def gravidade(update, context):
    pass

def prioridade(update, context):
    pass
    
def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text("Cancelou")
    
    return ConversationHandler.END    
    
def error(update, context):
    """Log de erros causados por Updates"""
    logger.warning('Update "%s" causou o erro "%s"', update, context.error)
    
def main():
    #token
    updater = Updater(token=telegram_token, use_context=True)
    
    #dispatcher
    dp = updater.dispatcher
    
    #add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        
        states={
            #relatando problema
            RELATAR_PROBLEMA: [MessageHandler(Filters.regex(r'Relatar problema'), relatar_problema)],
            COOP: [MessageHandler(Filters.text, cooperativa)],
            AREA: [MessageHandler(Filters.text, area)],
            DESCRICAO: [MessageHandler(Filters.text, descricao)],
            ANEXO: [MessageHandler(Filters.photo, anexo),
                    CommandHandler('skip', skip_anexo)],
            FREQUENCIA: [MessageHandler(Filters.text, freq)],
            #GRAVIDADE:
            #PRIORIDADE:
        },
        
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    dp.add_handler(conv_handler)
    dp.add_handler(CallbackQueryHandler(area))
    
    #log de todos erros
    dp.add_error_handler(error)    
    
    #inicia o bot    
    updater.start_polling()
    
    #bloqueio de execução
    updater.idle()
    
if __name__ == '__main__':
    main()
