import os
import ast
from telegram.ext import CommandHandler
from sheetsapi.simplesheetsapi.SheetsApi import SheetsApiTry
import telegram.ext


def start(update, conext):
    update.message.reply_text("Напишите /help")


def help(update, context):
    update.message.reply_text("""
    Пример использования команд:
    /get_cell_value A1 Sheet1 - получение содержимого ячейки
    /update_cell_value A1:A1 Sheet1 [["example"]] - изменение содержимого ячейки
    /find_rows_by Example_value Sheet1 - нахождение строки по содержимому одной из её ячеек
    """)


def get_cell_value(update, context):
    cell = update.message.text.split()[1]
    sheetname = update.message.text.split()[-1]
    col_id, row_id = cell[0], cell[1]
    value = sheet.get_cell(col_id, row_id, sheetname)
    update.message.reply_text(*value)


def update_cell_value(update, context):
    id_range = update.message.text.split()[1]
    sheetname = update.message.text.split()[2]
    values = ast.literal_eval(update.message.text.split()[-1])
    sheet.update_cell(id_range, sheetname, values)
    update.message.reply_text("Данные изменены")


def find_rows_by(update, context):
    value = update.message.text.split()[1]
    sheetname = update.message.text.split()[-1]
    rows = sheet.find_rows(value, sheetname)
    if rows:
        update.message.reply_text(rows)
    else:
        update.message.reply_text("Ничего не найдено")


def main():
    global sheet
    sheet = SheetsApiTry("1NPcJBlrHbeRwSnDajfuZtBmbWqcb2aUEdXjpxPEy02A", os.getcwd())
    updater = telegram.ext.Updater("5933754016:AAEywOG-jAuyOZbN6nqsYsYSMjg-wgLusTo")
    disp = updater.dispatcher
    disp.add_handler(CommandHandler('get_cell_value', get_cell_value))
    disp.add_handler(CommandHandler('start', start))
    disp.add_handler(CommandHandler("update_cell_value", update_cell_value))
    disp.add_handler(CommandHandler("find_rows_by", find_rows_by))
    disp.add_handler(CommandHandler("help", help))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
