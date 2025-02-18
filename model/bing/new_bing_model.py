# encoding:utf-8
import asyncio
from model.model import Model
from config import model_conf_val, common_conf_val, model_conf
from common import log, const
from EdgeGPT import Chatbot, ConversationStyle
from ImageGen import ImageGen
from common import functions
from model.bing.jailbroken_sydney import SydneyBot
import openai

user_session = dict()
suggestion_session = dict()
# newBing对话模型逆向网页gitAPI


class BingModel(Model):

    style = ConversationStyle.creative
    bot: Chatbot = None
    cookies: list = None

    def __init__(self):
        try:
            self.cookies = model_conf_val("bing", "cookies")
            self.jailbreak = model_conf_val("bing", "jailbreak")
            BingModel.style = model_conf_val("bing", "style")
            self.bot = SydneyBot(cookies=self.cookies, options={}) if (
                self.jailbreak) else Chatbot(cookies=self.cookies)
        except Exception as e:
            log.warn(e)

    async def reply_text_stream(self, query: str, context=None) -> dict:
        async def handle_answer(final, answer):
            if final:
                try:
                    reply = self.build_source_attributions(answer, context)
                    log.info("[NewBing] reply:{}", reply)
                    yield True, reply
                except Exception as e:
                    log.warn(answer)
                    log.warn(e)
                    await user_session.get(context['from_user_id'], None).reset()
                    yield True, answer
            else:
                try:
                    yield False, answer
                except Exception as e:
                    log.warn(answer)
                    log.warn(e)
                    await user_session.get(context['from_user_id'], None).reset()
                    yield True, answer

        if not context or not context.get('type') or context.get('type') == 'TEXT':
            clear_memory_commands = common_conf_val(
                'clear_memory_commands', ['#清除记忆'])
            if query in clear_memory_commands:
                user_session[context['from_user_id']] = None
                yield True, '记忆已清除'
            bot = user_session.get(context['from_user_id'], None)
            if not bot:
                bot = self.bot
            else:
                query = self.get_quick_ask_query(query, context)
            user_session[context['from_user_id']] = bot
            log.info("[NewBing] query={}".format(query))
            if self.jailbreak:
                async for final, answer in bot.ask_stream(query, conversation_style=self.style, message_id=bot.user_message_id):
                    async for result in handle_answer(final, answer):
                        yield result
            else:
                async for final, answer in bot.ask_stream(query, conversation_style=self.style):
                    async for result in handle_answer(final, answer):
                        yield result

    def reply(self, query: str, context=None) -> tuple[str, dict]:
        if not context or not context.get('type') or context.get('type') == 'TEXT':
            clear_memory_commands = common_conf_val(
                'clear_memory_commands', ['#清除记忆'])
            if query in clear_memory_commands:
                user_session[context['from_user_id']] = None
                return '记忆已清除'
            bot = user_session.get(context['from_user_id'], None)
            if (bot == None):
                bot = self.bot
            else:
                query = self.get_quick_ask_query(query, context)

            user_session[context['from_user_id']] = bot
            log.info("[NewBing] query={}".format(query))
            if (self.jailbreak):
                task = bot.ask(query, conversation_style=self.style,
                               message_id=bot.user_message_id)
            else:
                task = bot.ask(query, conversation_style=self.style)

            answer = asyncio.run(task)
            if isinstance(answer, str):
                return answer
            try:
                reply = answer["item"]["messages"][-1]
            except Exception as e:
                user_session.get(context['from_user_id'], None).reset()
                log.warn(answer)
                return "本轮对话已超时，已开启新的一轮对话,请重新提问。"
            return self.build_source_attributions(answer, context)
        elif context.get('type', None) == 'IMAGE_CREATE':
            if functions.contain_chinese(query):
                log.info('翻译prompt为英文');
                try:
                    openai.api_key = model_conf(const.OPEN_AI).get('api_key')
                    openai.organization = model_conf(const.OPEN_AI).get('organization')
                    res = openai.ChatCompletion.create(
                        model=model_conf(const.OPEN_AI).get("model") or "gpt-3.5-turbo",  # 对话模型的名称
                        messages=[
                            {"role": "system", "content": "从现在开始，你是一名中英翻译，你会根据我输入的中文内容，翻译成对应英文。请注意，你翻译后的内容主要服务于一个绘画AI，它只能理解具象的描述而非抽象的概念，同时根据你对绘画AI的理解，比如它可能的训练模型、自然语言处理方式等方面，进行翻译优化。由于我的描述可能会很散乱，不连贯，你需要综合考虑这些问题，然后对翻译后的英文内容再次优化或重组，从而使绘画AI更能清楚我在说什么。同时还需要注意一些特殊中文词语的意思，不能简单的进行字面翻译，如夫妻肺片不可以翻译成Husband and Wife Lung Slices而应该翻译成Sichuan Sliced Beef in Chili Sauce。请严格按照此条规则进行翻译，也只输出翻译后的英文内内容。"},
                            {"role": "user", "content": query}
                        ]
                    )
                    query = res.choices[0]['message']['content']
                except Exception as e:
                    log.warn(e)
                    return "ImageGen目前仅支持使用英文关键词生成图片"
            return self.create_img(query)

    def create_img(self, query):
        try:
            log.info("[NewBing] image_query={}".format(query))
            cookie_value = self.cookies[0]["value"]
            image_generator = ImageGen(cookie_value)
            img_list = image_generator.get_images(query)
            log.info("[NewBing] image_list={}".format(img_list))
            return img_list
        except Exception as e:
            log.warn(e)
            return "输入的内容可能违反微软的图片生成内容策略。过多的策略冲突可能会导致你被暂停访问。"

    def get_quick_ask_query(self, query, context):
        if (len(query) == 1 and query.isdigit() and query != "0"):
            suggestion_dict = suggestion_session[context['from_user_id']]
            if (suggestion_dict != None):
                query = suggestion_dict[int(query)-1]
                if (query == None):
                    return "输入的序号不在建议列表范围中"
                else:
                    query = "在上面的基础上，"+query
        return query

    def build_source_attributions(self, answer, context):
        reference = ""
        reply = answer["item"]["messages"][-1]
        reply_text = reply["text"]
        if "sourceAttributions" in reply:
            for i, attribution in enumerate(reply["sourceAttributions"]):
                display_name = attribution["providerDisplayName"]
                url = attribution["seeMoreUrl"]
                reference += f"{i+1}、[{display_name}]({url})\n\n"

            if len(reference) > 0:
                reference = "***\n"+reference

            suggestion = ""
            if "suggestedResponses" in reply:
                suggestion_dict = dict()
                for i, attribution in enumerate(reply["suggestedResponses"]):
                    suggestion_dict[i] = attribution["text"]
                    suggestion += f">{i+1}、{attribution['text']}\n\n"
                suggestion_session[context['from_user_id']
                                   ] = suggestion_dict

            if len(suggestion) > 0:
                suggestion = "***\n你可以通过输入序号快速追问我以下建议问题：\n\n"+suggestion

            throttling = answer["item"]["throttling"]
            throttling_str = ""

            if throttling["numUserMessagesInConversation"] == throttling["maxNumUserMessagesInConversation"]:
                user_session.get(context['from_user_id'], None).reset()
                throttling_str = "(对话轮次已达上限，本次聊天已结束，将开启新的对话)"
            elif not self.jailbreak: # 因为当开启 jailbreak 轮次始终为1 不需要统计
                throttling_str = f"对话轮次: {throttling['numUserMessagesInConversation']}/{throttling['maxNumUserMessagesInConversation']}\n"

            response = f"{reply_text}\n{reference}\n{suggestion}\n***\n{throttling_str}"
            log.info("[NewBing] reply={}", response)
            return response
        else:
            user_session.get(context['from_user_id'], None).reset()
            log.warn("[NewBing] reply={}", answer)
            return "对话被接口拒绝，已开启新的一轮对话。"
