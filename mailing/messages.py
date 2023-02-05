from collections import defaultdict
from keyboards import mailing
msgs = defaultdict(lambda: None)
msgs['helloMsg1'] = defaultdict(lambda: None, {
    'text':'⚡️ <b>СЕЗОН "ВЕСНА" - "ОСЕНЬ"</b>\n➖➖➖➖➖➖➖➖➖➖➖➖\n\nЗаменим резину и масло со <b>скидкой в 60%</b>\n\nСтаньте участником клуба, чтобы получить скидку 👇🏼',
    'keyboard': 'keyboardHelloMailing',
    'nextMsg': 'helloMsg2',
    'delay': 60, #24*60*60
    'state':'notVip',
    'photo':'pictures/how_to3.jpg'
})

msgs['helloMsg2'] = defaultdict(lambda: None,{
    'text':'⚡️ ДЛЯ КОГО ПОДОЙДЕТ НАША КАРТА\n➖➖➖➖➖➖➖➖➖➖➖➖\n\n1. Бизнесмен и руководитель\n2. Женщина и девушка за рулем\n3. Путешественники и командировочные\n4. Начинающий водитель\n5. Машина есть, вникать в хлопоты не хочется\n6. Для кого ситуации на дороге – стресс и беспокойство\n7. Подарок жене/мужу/детям/родителям\n8.Парень с хорошей машиной',
    'keyboard': 'keyboardHelloMailing',
    'nextMsg': 'helloMsg3',
    'delay': 60, #2*24*60*60
    'state':'notVip',
    'photo':'pictures/how_to3.jpg'
})

msgs['helloMsg3'] = defaultdict(lambda: None,{
    'text':'⚡️ АКЦИЯ ОТ СТРАХОВЩИКА  ➖➖➖➖➖➖➖➖➖➖➖➖   *тут будет текст*',
    'keyboard': 'keyboardHelloMailing',
    'nextMsg': 'freeWeek',
    'delay': 60, #3*24*60*60
    'state':'notVip',
    'video':'pictures/video.mp4',
    'photo':'pictures/how_to3.jpg'
})

msgs['freeWeek'] = defaultdict(lambda: None,{
    'text':'⚡️ ТЕСТОВАЯ НЕДЕЛЯ\n➖➖➖➖➖➖➖➖➖➖➖➖\n\n*тут будет про тестовую неделю бесплатно*',
    'keyboard': 'keyboardHelloMailing',
    'nextMsg': None,
    'delay': 60, #2*24*60*60
    'state':'notVip',
    'photo':'pictures/how_to3.jpg'
})

msgs['getPhone'] = defaultdict(lambda: None,{
    'text':'❗️ЕЩЕ СОМНЕВАЕТЕСЬ? ПРОЧТИТЕ ЭТО❗\n\nСтоимость карты - <b>500 рублей в месяц</b> <i>*это 16 рублей в день</i>\nЗа эти деньги вы получите:\n- техническую и правовую поддержку на дороге,\n- уверенность и спокойствие в любой неприятной ситуации на дороге,\n- вы не тратите свое время на поиск выгодных условий в  автосервисах, автомойках, страховых компаниях,\n- и не переплачиваете за них по незнанию.\n\n<b>Скажите, вы готовы перейти к оформлению тарифа?</b>',
    'keyboard': 'keyboardReadThis',
    'nextMsg': None,
    'delay': 60, #2*60*60
    'state':'notVip',
})
def get_text_end1(name):
    return f'Добрый день {name} ⚡️\n\nХочу напомнить, зачем мы создали этот клуб.\n\n1. <b>Проверенные партнеры</b>, которые на связи 24 часа в сутки по любому вашему вопросу.\n2. <b>Экономия на покупках</b>. Зачем переплачивать, если с нами дешевле?\n3. Окружение крутых людей, с кем вам будет о чем поговорить и у кого будет спросить совет.\n\nСкорее нажимайте кнопку и вступайте в клуб 👇🏼'


msgs['vipEnd1'] = defaultdict(lambda :None, {
    'text': get_text_end1,
    'keyboard': 'keyboardVipEnd1',
    'nextMsg': 'vipEnd2',
    'delay': 60,  # 24*60*60
    'state': 'notVip',
    'photo': 'pictures/endVip1.jpg'
})


def get_text_end2(name):
    return f'Приветствую {name} ☺️\n\nЕсли у вас какие-либо <b>технические вопросы</b> или вопросы по <b>дальнейшему продлению</b>, вы можете написать нам.\n\nНиже оставлю кнопку, по которой вы сможете связаться с нами на прямую 🗳'



msgs['vipEnd2'] = defaultdict(lambda :None, {
    'text': get_text_end2,
    'keyboard': 'keyboardVipEnd2',
    'nextMsg': 'vipEnd3',
    'delay': 60,  # 5*24*60*60
    'state': 'notVip',
    'photo': 'pictures/how_to3.jpg'
})


msgs['vipEnd3'] = defaultdict(lambda :None, {
    'text': 'Вот уже как неделю я грущу без вас 🥺\n\nВы можете сказать, да ладно тебе, ты просто бездушный робот.\n\n🤖 Да, я робот, но не бездушный и я переживаю, что не состоя в клубе, вы переплачиваете за все подряд и подвергаетесь риску мошенников.\n\nЕще не поздно вернуться 👇🏼',
    'keyboard': 'keyboardVipEnd2',
    'nextMsg': 'vipEnd4',
    'delay': 60,  # 7*24*60*60
    'state': 'notVip',
    'photo': 'pictures/endVip3.jpg'
})


msgs['vipEnd4'] = defaultdict(lambda :None, {
    'text': '💰 КАК СЭКОНОМИТЬ ОТ 5000 рублей в месяц?\n\n*а это 60 000 в год. \n\nИменно столько в среднем экономят участники нашего сообщества при участии и покупки у наших партнеров.\n\nРассчитать свою экономию вы можете по кнопке ниже 👇🏼',
    'keyboard': 'keyboardVipEnd1',
    'nextMsg': None,
    'delay': 60,  # 7*24*60*60
    'state': 'notVip',
    'photo': 'pictures/endVip4.jpg'
})




async def get_text_vipEnd1(name, delay):
    return defaultdict(lambda :None, {
    'text':f'Добрый день {name}⚡️\n\nЧерез 1 день я буду вынужден отключить вас от нашего канал и закрыть доступ к партнёрам.\n➖➖➖➖➖➖➖➖➖➖➖➖\n\nОставайтесь с нами в клубе, переходите по кнопке и продлевайте вашу экономию! 👇🏼',
    'state':'toVip3Day',
    'photo':'pictures/toVip1.jpg',
    'keyboard':'keyboardToVip',
    'delay':delay,
})



async def get_text_vipEnd3(name, delay):
    return defaultdict(lambda :None, {
    'text':f'Добрый день {name} ⚡️\n\nНапоминаю вам, что ваша подписка закончится через 3 дня.\n➖➖➖➖➖➖➖➖➖➖➖➖\n\n!!️Не забудьте оплатить, чтобы сохранить все акции от партнёров.',
    'state':'toVip3Day',
    'photo':'pictures/toVip2.jpg',
    'keyboard':'keyboardToVip',
    'delay':delay,
})

