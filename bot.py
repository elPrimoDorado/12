import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import os
import time
from buttons import *

# env
bot_token = os.environ.get("TOKEN", "") 
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")

# bot
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)
MESGS = {}

# enlace
@app.on_message(filters.command(['enlace']))
def help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    try:
        with open("enlaces.txt", 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()  # Elimina espacios en blanco y saltos de línea
                if "https://t.me/c/" in line:
                    app.send_message(message.chat.id, "**Send me only Public Channel Links**")
                else:
                    datas = line.split("/")
                    msgid = int(datas[-1])
                    print(datas)
                    print(msgid)
                    username = datas[-2]
                    print(username)
                    

                    try:
                        msg = app.get_messages(username, msgid)
                        app.copy_message(message.chat.id, msg.chat.id, msg.id)
                    except Exception as e:
                        print(f"Error al copiar el mensaje: {str(e)}")
                    time.sleep(4)  # Espera 4 segundos entre cada mensaje

                    
    except Exception as e:
        print(f"Error al enviar mensajes desde el archivo: {str(e)}")


@app.on_message(filters.command(['reenviar']))
def procesar_enlaces(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    try:
        message.reply("Por favor, proporciona el nombre del canal, el número de inicio y el número final separados por espacios.")
        
        @app.on_message(filters.text)
        def obtener_parametros(client: pyrogram.client.Client, msg: pyrogram.types.messages_and_media.message.Message):
            parametros = msg.text.strip().split()
            
            if len(parametros) != 3:
                msg.reply("Debes proporcionar el nombre del canal, el número de inicio y el número final separados por espacios.")
                return
            
            canal = parametros[0]
            try:
                canal_info = app.get_chat(canal)
                canal_type = str(canal_info.type)
                print(canal_info)
                print(canal_info.type)
                
                # Verificar si el canal es privado
                if canal_type == "ChatType.PRIVATE":
                    print("Esprivado")
                    
                    msg.reply("El canal es privado y no puedo acceder a él.")
                    return
            except pyrogram.errors.ChatAdminRequired as e:
                msg.reply("El canal no existe o no tengo permisos para acceder a él.")
                return
            except pyrogram.errors.UsernameInvalid as e:
                msg.reply("El nombre del canal es inválido.")
                return
            except Exception as e:
                    app.send_message(message.chat.id, f"Error desconocido {enlace}.")
                    
                    print(f"Errr")

            try:
                inicio = int(parametros[1])
                final = int(parametros[2])
            except ValueError:
                msg.reply("El número de inicio y el número final deben ser valores enteros válidos.")
                return
             # Establece un límite máximo de 5000
            limite_maximo = 5000
            if final - inicio > limite_maximo:
                msg.reply(f"La diferencia entre el número de inicio y el número final no debe ser mayor que {limite_maximo}.")
                return
            if final < inicio:
                msg.reply(f"El numero inicial no puede ser mayor que el final {limite_maximo}.")
                return
            
            for i in range(inicio, final + 1):
                enlace = f"https://t.me/{canal}/{i}"
                try:
                    msg = app.get_messages(canal, i)
                    app.copy_message(message.chat.id, msg.chat.id, msg.id)
                    time.sleep(4)  # Espera 4 segundos entre cada mensaje
                except Exception as e:
                    app.send_message(message.chat.id, f"Mensaje eliminado o no existe {enlace}.")
                    
                    print(f"Error al copiar el mensaje: {str(e)}")
            
            app.remove_handler(obtener_parametros)
    
    except Exception as e:
        print(f"Error al procesar enlaces: {str(e)}")

# app messages
@app.on_message(filters.command(['start']))
def start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, f"Bienvenido {message.from_user.mention}\nSigue las intrucciones del archivo readme en github antes de desplegar el bot__", reply_to_message_id=message.id)
                
# callback
@app.on_callback_query()
def inbtwn(client: pyrogram.client.Client, call: pyrogram.types.CallbackQuery):
    print("En funcion callback linea 377")

#apprun
print("Bot Started")
app.run()
