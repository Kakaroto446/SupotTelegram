# -*- coding: utf-8 -*-
# File: postman.py
# Created by: Johnny Barbosa
# Date: 07/11/2019
# Description: Contains all the functions responsibilities for send the bug reports.

import logging
from credentials import *
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

campos = ["Usuário",
          "Cooperativa",
          "Área",
          "Descrição",
          "Anexo"]

lista = []

text = """
*[RELATÓRIO DE ERRO]*
*Usuário:* {0[0]}
*Cooperativa:* {0[1]}
*Área:* {0[2]}
*Descriçao:* {0[3]}
*Anexo:* {0[4]}
*Frequência: * {0[5]}
"""

def env_relatorio(cod, x): #envia pelo telegram o relatório
    bot = telegram.Bot(token = telegram_token)
    if cod == 5: #anexo
        bot.sendMessage(chat_id=chat_id, text=text.format(lista), parse_mode=telegram.ParseMode.MARKDOWN)
        
    if cod <= 6:
        lista.append(x)
    else: 
        lista.append(x)
        bot.sendMessage(chat_id=chat_id, text=text.format(lista), parse_mode=telegram.ParseMode.MARKDOWN)
        

def write(cod, x): #cria um arquivo txt com o relatório de erro
    #aqui é verificado se é os dados estão vindo da mensagem de start ou do resto da conversa
    #se cod = 0 tá no start, abre o arquivo em w+ pra apagar o que tem e ficar em rw
    #else abre em r+ pra ficar em rw sem apagar o conteúdo
    if cod == 0:
        arquivo = open('email.txt', 'w+')
    else:
        arquivo = open('email.txt', 'r+')
    #escrita dos dados    
    texto = "{}: {}\n".format(campos[cod], x)
    conteudo = arquivo.readlines()
    print("conteudo antigo: \n", conteudo)
    conteudo.append(texto)
    print("conteudo novo: \n", conteudo)
    arquivo.writelines(conteudo)
    
    
    ##teste
    
    
    ## Abra o arquivo (leitura)
    #arquivo = open('email.txt', 'r')
    #conteudo = arquivo.readlines()
    
    ## insira seu conteúdo
    ## obs: o método append() é proveniente de uma lista
    #texto = "{}: {}\n".format(campos[cod], x)
    #conteudo.append(texto)
    
    ## Abre novamente o arquivo (escrita)
    ## e escreva o conteúdo criado anteriormente nele.
    #arquivo = open('email.txt', 'w')
    #arquivo.writelines(conteudo)
    #arquivo.close()    
    
    arquivo.close()    
    
    # koreturn