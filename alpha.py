# Модули
import telebot
import time

# Бот
API_TOKEN = '_'
bot = telebot.TeleBot(API_TOKEN)
user_data = {}
recipient = _

# Функции
def animation(message):
	bot.send_chat_action(chat_id=recipient, action='upload_video')
	file_id = message.animation.file_id
	bot.send_animation(chat_id=recipient, animation=file_id)
#
def audio(message):
	bot.send_chat_action(chat_id=recipient, action='upload_voice')
	file_id = message.audio.file_id
	bot.send_audio(chat_id=recipient, audio=file_id)
#
def contact(message):
	bot.send_chat_action(chat_id=recipient, action='upload_document')
	phone_number = message.contact.phone_number
	first_name = message.contact.first_name
	last_name = message.contact.last_name
	bot.send_contact(
		chat_id=recipient,
		phone_number=phone_number,
		first_name=first_name,
		last_name=last_name)
#
def dice(message):
	bot.send_chat_action(chat_id=recipient, action='choose_sticker')
	emoji = message.dice.emoji
	value = message.dice.value
	message_id = message.message_id
	bot.send_message(recipient, emoji)
	bot.send_message(recipient, f'Значение: {value}', reply_to_message_id=message_id + 1)
#
def document(message):
	bot.send_chat_action(chat_id=recipient, action='upload_document')
	file_id = message.document.file_id
	bot.send_document(chat_id=recipient, document=file_id)
#
def location(message):
	bot.send_chat_action(chat_id=recipient, action='find_location')
	latitude = message.location.latitude
	longitude = message.location.longitude
	bot.send_location(chat_id=recipient, latitude=latitude, longitude=longitude)
#
def text(message):
	bot.send_chat_action(chat_id=recipient, action='typing')
	text = message.text
	bot.send_message(recipient, text)
#
def photo(message):
	bot.send_chat_action(chat_id=recipient, action='upload_photo')
	file_id = message.photo[-1].file_id
	bot.send_photo(chat_id=recipient, photo=file_id)
#
def poll(message):
	bot.send_chat_action(chat_id=recipient, action='typing')
	poll = message.poll
	question = f'Вопрос: {poll.question}\n\n'
	answers = 'Варианты ответов:\n'
	report = question + answers

	for option in poll.options:
		count = option.voter_count
		if (count % 10 == 1) and (count % 100 != 11):
			suffix = 'голос'
		elif (2 <= count % 10 <= 4) and (not (12 <= count % 100 <= 14)):
			suffix = 'голоса'
		else:
			suffix = 'голосов'
		report += f"{option.text}: {count} {suffix}\n"

	bot.send_poll(
		chat_id=recipient,
		question=poll.question,
		options=[option.text for option in poll.options],
		is_anonymous=poll.is_anonymous,
		type=poll.type,
		allows_multiple_answers=poll.allows_multiple_answers,
		correct_option_id=poll.correct_option_id if poll.type == 'quiz' else None,
		explanation=poll.explanation or None)
	bot.send_message(message.chat.id, report, reply_to_message_id=message.message_id + 1)
#
def sticker(message):
	bot.send_chat_action(chat_id=recipient, action='choose_sticker')
	file_id = message.sticker.file_id
	bot.send_sticker(chat_id=recipient, sticker=file_id)
#
def venue(message):
	bot.send_chat_action(chat_id=recipient, action='find_location')
	latitude = message.venue.location.latitude
	longitude = message.venue.location.longitude
	title = message.venue.title
	address = message.venue.address
	bot.send_venue(
		chat_id=recipient,
		latitude=latitude,
		longitude=longitude,
		title=title,
		address=address)
#
def video(message):
	bot.send_chat_action(chat_id=recipient, action='upload_video')
	file_id = message.video.file_id
	bot.send_video(chat_id=recipient, video=file_id)
#
def video_note(message):
	bot.send_chat_action(recipient, 'upload_video_note')
	file_id = message.video_note.file_id
	bot.send_video_note(recipient, file_id)
#
def voice(message):
	bot.send_chat_action(chat_id=recipient, action='upload_voice')
	file_id = message.voice.file_id
	bot.send_voice(chat_id=recipient, voice=file_id)
#
def main():
	while True:
		try:
			bot.infinity_polling()
		except:
			time.sleep(180)
	
# Хэндлеры
@bot.message_handler(commands=['start'])
def welcome(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	from_user_id = message.from_user.id
	first_name = message.from_user.first_name
	bot.reply_to(message, f'Здравствуйте, {first_name}!\nВаш ID: {from_user_id}')
#
@bot.message_handler(commands=['recipient'])
def recipient(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	bot.reply_to(message, 'Отправьте мне пожалуйста ID Получателя!')
	bot.register_next_step_handler(message, get_recipient_id)
#
def get_recipient_id(message):
	if message == '/start':
		welcome(message)
		return None
	user_id = message.from_user.id
	recipient = message.text.strip()
	
	if (recipient.isdigit()) and (1 <= int(recipient) <= 2_147_483_647):
		user_data[user_id] = {'recipient': recipient}
		bot.send_message(user_id, 'Получатель изменён!')
	else:
		bot.send_message(user_id, "Некорректный ID. Пожалуйста, введите число от 1 до 2'147'483'647.")
		bot.register_next_step_handler(message, get_recipient_id)
#
@bot.message_handler(content_types=[
	'animation', 'audio', 'contact', 'dice',
	'document', 'location', 'photo', 'text',
	'sticker', 'venue', 'video', 'video_note',
	'voice', 'poll'])
def universal_handler(message):
	if message.animation:
		animation(message)
	elif message.audio:
		audio(message)
	elif message.contact:
		contact(message)
	elif message.dice:
		dice(message)
	elif message.document:
		document(message)
	elif message.location:
		location(message)
	elif message.photo:
		photo(message)
	elif message.text:
		text(message)
	elif message.sticker:
		sticker(message)
	elif message.venue:
		venue(message)
	elif message.video:
		video(message)
	elif message.video_note:
		video_note(message)
	elif message.voice:
		voice(message)
	elif message.poll:
		poll(message)

# Пуллинг
if __name__ == "__main__":
	main()
