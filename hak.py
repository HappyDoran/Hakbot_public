import discord
from discord.ext import commands
import shutil
import re
import json
from discord_buttons_plugin import *
import uuid

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="~", intents=intents)
buttons = ButtonsClient(bot)
token = "token"


@bot.event
async def on_ready():
    print(bot.user.name, "has connected to Discord.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('도움말 명령어는 ~도움말'))
    print('[알림]학 봇 "ON"')


@bot.event
async def on_message(msg):
    if msg.author.bot: return None
    await bot.process_commands(msg)


@bot.command()
async def 등록(ctx):
    id = ctx.message.author.id
    nick = ctx.message.author.nick
    subnick = ctx.message.author.mention
    if not nick:
        nick = ctx.message.author.name

    file_path = "data.json"
    file_path3 = "three_month_data.json"

    with open(file_path) as f:
        df = json.load(f)

    with open(file_path3) as f:
        df2 = json.load(f)

    if not df:
        df['{0}'.format(id)] = {
            'nickname': nick,
            'subnickname': subnick,
            'cnt': 0,
        }
        df2['{0}'.format(id)] = {
            'nickname': nick,
            'subnickname': subnick,
            'cnt': 0,
            'our': 0,
        }
        await ctx.message.delete()
        await ctx.channel.send(f"정보 저장 완료! {ctx.message.author.mention}님 반갑습니다!")

    else:
        if df.get('{0}'.format(id)) == None:

            df['{0}'.format(id)] = {
                'nickname': nick,
                'subnickname': subnick,
                'cnt': 0,
            }
            df2['{0}'.format(id)] = {
                'nickname': nick,
                'subnickname': subnick,
                'cnt': 0,
                'our': 0,
            }
            await ctx.message.delete()
            await ctx.channel.send(f"정보 저장 완료! {ctx.message.author.mention}님 반갑습니다!")

        else:
            df.get('{0}'.format(id))['subnickname'] = subnick
            df2.get('{0}'.format(id))['subnickname'] = subnick

            await ctx.message.delete()
            await ctx.channel.send(f"{ctx.message.author.mention}님, 이미 저장되어 있는 사용자 입니다!")

    with open(file_path, 'w') as f:
        json.dump(df, f, indent=2, ensure_ascii=False)

    with open(file_path3, 'w') as f:
        json.dump(df2, f, indent=2, ensure_ascii=False)


@bot.command()
async def 삭제(ctx, *input):
    rdid = re.compile('<@(?P<did>\w+)>')
    des = ' '.join(list(input))
    reg = rdid.search(des)
    tDid = reg.group('did')
    trealDid = f'<@{tDid}>'

    id = ctx.message.author.id
    guild = ctx.message.guild
    member = guild.get_member(id)

    permission = 0

    try:
        for role in member.roles:
            if permission < role.position:
                permission = role.position

    except:
        pass

    file_path = "User.json"
    file_path3 = "three_month_data.json"

    if permission >= 9 or guild.owner_id == id:
        with open(file_path) as f:
            df = json.load(f)

        with open(file_path3) as f:
            df2 = json.load(f)

        df.pop(tDid)
        df2.pop(tDid)

        await ctx.message.delete()
        await ctx.channel.send(f"{trealDid}님 삭제 완료.")

        with open(file_path, 'w') as f:
            json.dump(df, f, indent=2, ensure_ascii=False)

        with open(file_path3, 'w') as f:
            json.dump(df, f, indent=2, ensure_ascii=False)

    else:
        await ctx.channel.send(f"{ctx.message.author.mention}님은 권한이 없습니다!")


@bot.command()
async def 강제등록(ctx, *input):
    rdid = re.compile('<@(?P<did>\w+)>')
    des = ' '.join(list(input))
    reg = rdid.search(des)
    tDid = reg.group('did')
    trealDid = f'<@{tDid}>'
    print(trealDid)
    # await ctx.channel.send(f"디스코드 회원 번호 {tDid}입니다.")

    file_path = "data.json"
    file_path3 = "three_month_data.json"

    with open(file_path) as f:
        df = json.load(f)

    with open(file_path3) as f:
        df2 = json.load(f)

    if not df:
        df['{0}'.format(tDid)] = {
            'nickname': "의문의 사나이",
            'subnickname': trealDid,
            'cnt': 0,
        }
        df2['{0}'.format(tDid)] = {
            'nickname': "의문의 사나이",
            'subnickname': trealDid,
            'cnt': 0,
            'our': 0,
        }
        await ctx.message.delete()
        await ctx.channel.send(f"정보 저장 완료! 디비접근해서 닉네임 바꾸세요")

    else:
        if df.get('{0}'.format(tDid)) == None:

            df['{0}'.format(tDid)] = {
                'nickname': "의문의 사나이",
                'subnickname': trealDid,
                'cnt': 0,
            }
            df2['{0}'.format(tDid)] = {
                'nickname': "의문의 사나이",
                'subnickname': trealDid,
                'cnt': 0,
                'our': 0,
            }
            await ctx.message.delete()
            await ctx.channel.send(f"정보 저장 완료! 디비접근해서 닉네임 바꾸세요")

        else:
            df.get('{0}'.format(tDid))['subnickname'] = trealDid
            df2.get('{0}'.format(tDid))['subnickname'] = trealDid

            await ctx.message.delete()
            await ctx.channel.send(f"{trealDid}님, 이미 저장되어 있는 사용자 입니다!")

    with open(file_path, 'w') as f:
        json.dump(df, f, indent=2, ensure_ascii=False)

    with open(file_path3, 'w') as f:
        json.dump(df2, f, indent=2, ensure_ascii=False)


@bot.command()
async def 친선기록(ctx, *input):
    rMonth = re.compile('(?P<month>\d+)월')
    rDate = re.compile('(?P<date>\d+)일')
    rTime = re.compile('(?P<time>\d+)시')
    rWho = re.compile('vs\s(?P<who>\w+)')

    des = ' '.join(list(input))
    reg = rWho.search(des)
    tWho = reg.group('who')

    member = []
    member_did = []
    flag = 0

    tMonth = None
    tDate = None
    tTime = None

    file_path = "data.json"
    file_path3 = "three_month_data.json"

    with open(file_path) as f:
        df = json.load(f)

    with open(file_path3) as f:
        df2 = json.load(f)

    for i in input:
        id = 0
        opt = 0
        if (rMonth.search(i) or rDate.search(i) or rTime.search(i)):
            try:
                reg = rMonth.search(i)
                tMonth = reg.group('month')
            except:
                pass
            try:
                reg = rDate.search(i)
                tDate = reg.group('date')
            except:
                pass
            try:
                reg = rTime.search(i)
                tTime = reg.group('time')

            except:
                pass
        else:
            if i == 'vs' or i == tWho:
                continue
            else:
                for index, (key, elem) in enumerate(df.items()):
                    if i == elem['nickname']:
                        id = key
                        opt = 1
                    elif i == elem['subnickname']:
                        id = key
                        opt = 2
                if id == 0:
                    await ctx.message.delete()
                    await ctx.channel.send("{0}은(는) 등록되어 있지 않은 사용자입니다! 다른 이름으로 등록되어있는지 확인해주세요!".format(i))
                    flag = 1
                else:
                    if opt == 1:
                        member.append(i)
                        member_did.append(id)
                    elif opt == 2:
                        member.append(df.get('{0}'.format(id))['nickname'])
                        member_did.append(id)

    if tMonth == None or tDate == None or tTime == None:
        await ctx.message.delete()
        await ctx.channel.send("날짜를 정확하게 입력해주세요!")
        flag = 1

    if flag == 0:
        for i in range(len(member)):
            df.get('{0}'.format(member_did[i]))['cnt'] = df.get('{0}'.format(member_did[i]))['cnt'] + 1
            df2.get('{0}'.format(member_did[i]))['cnt'] = df2.get('{0}'.format(member_did[i]))['cnt'] + 1

        if len(member) < 4:
            for i in range(4 - len(member)):
                member.append(" ")

        with open(file_path, 'w') as f:
            json.dump(df, f, indent=2, ensure_ascii=False)

        with open(file_path3, 'w') as f:
            json.dump(df2, f, indent=2, ensure_ascii=False)

        time = '{0}.{1}.{2}:00'.format(tMonth, tDate, tTime)
        record_path = "Record.json"
        member_str = " ".join(map(str, member))

        with open(record_path) as f:
            df = json.load(f)

        if not df:
            df['{0}'.format(uuid.uuid4())] = {
                'time': time,
                'vs': tWho,
                'member': member,
            }

        else:
            df['{0}'.format(uuid.uuid4())] = {
                'time': time,
                'vs': tWho,
                'member': member,
            }

        with open(record_path, 'w') as f:
            json.dump(df, f, indent=2, ensure_ascii=False)

        try:
            url = ctx.message.attachments[0].url
        except IndexError:
            embed = discord.Embed(title='🫰친선 임베드 ',
                                  description="\n\n**친선 시간**\n{0}월 {1}일 {2}시\n"
                                              "\n**VS**\n{3}\n"
                                              "\n**멤버**\n{4}\n"
                                              "\n**기록 완료**\n".format(tMonth, tDate, tTime, tWho,
                                                                     member_str),

                                  color=0x62c1cc)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed)
        else:
            if url[0:26] == "https://cdn.discordapp.com":  # look to see if url is from discord
                embed = discord.Embed(title='🫰친선 임베드 ',
                                      description="\n\n**친선 시간**\n{0}월 {1}일 {2}시\n"
                                                  "\n**VS**\n{3}\n"
                                                  "\n**멤버**\n{4}\n"
                                                  "\n**기록 완료**\n".format(tMonth, tDate, tTime, tWho,
                                                                         member_str),
                                      color=0x62c1cc)
                embed.set_image(url=url)
                await ctx.message.delete()
                await ctx.channel.send(embed=embed)


@bot.command()
async def 내전(ctx, *input):
    rMonth = re.compile('(?P<month>\d+)월')
    rDate = re.compile('(?P<date>\d+)일')
    rTime = re.compile('(?P<time>\d+)시')
    rCount = re.compile('(?P<count>\d+)번')

    member = []
    member_did = []
    flag = 0

    tMonth = None
    tDate = None
    tTime = None

    file_path = "data.json"
    file_path3 = "three_month_data.json"

    with open(file_path) as f:
        df = json.load(f)

    with open(file_path3) as f:
        df2 = json.load(f)

    for i in input:
        id = 0
        opt = 0
        if (rMonth.search(i) or rDate.search(i) or rTime.search(i) or rCount.search(i)):
            try:
                reg = rMonth.search(i)
                tMonth = reg.group('month')
            except:
                pass
            try:
                reg = rDate.search(i)
                tDate = reg.group('date')
            except:
                pass
            try:
                reg = rTime.search(i)
                tTime = reg.group('time')
            except:
                pass
            try:
                reg = rCount.search(i)
                tCount = reg.group('count')
            except:
                pass
        else:
            for index, (key, elem) in enumerate(df.items()):
                if i == elem['nickname']:
                    id = key
                    opt = 1
                elif i == elem['subnickname']:
                    id = key
                    opt = 2
            if id == 0:
                await ctx.message.delete()
                await ctx.channel.send("{0}은(는) 등록되어 있지 않은 사용자입니다! 다른 이름으로 등록되어있는지 확인해주세요!".format(i))
                flag = 1
            else:
                if opt == 1:
                    member.append(i)
                    member_did.append(id)
                elif opt == 2:
                    member.append(df.get('{0}'.format(id))['nickname'])
                    member_did.append(id)

    if tMonth == None or tDate == None or tTime == None:
        await ctx.message.delete()
        await ctx.channel.send("날짜를 정확하게 입력해주세요!")
        flag = 1

    if flag == 0:
        for i in range(len(member)):
            df.get('{0}'.format(member_did[i]))['cnt'] = df.get('{0}'.format(member_did[i]))['cnt'] + int(tCount)
            df2.get('{0}'.format(member_did[i]))['our'] = df2.get('{0}'.format(member_did[i]))['our'] + 1

        if len(member) < 8:
            for i in range(8 - len(member)):
                member.append(" ")

        with open(file_path, 'w') as f:
            json.dump(df, f, indent=2, ensure_ascii=False)

        with open(file_path3, 'w') as f:
            json.dump(df2, f, indent=2, ensure_ascii=False)

        time = '{0}.{1}.{2}:00'.format(tMonth, tDate, tTime)
        record_path = "Record.json"

        with open(record_path) as f:
            df = json.load(f)

        if not df:
            df['{0}'.format(uuid.uuid4())] = {
                'time': time,
                'vs': '내전',
                'member': member,
            }

        else:
            df['{0}'.format(uuid.uuid4())] = {
                'time': time,
                'vs': '내전',
                'member': member,
            }

        with open(record_path, 'w') as f:
            json.dump(df, f, indent=2, ensure_ascii=False)

        try:
            url = ctx.message.attachments[0].url
        except IndexError:
            embed = discord.Embed(title='🫰내전 임베드 ',
                                  description="\n\n**친선 시간**\n{0}월 {1}일 {2}시\n"
                                              "\n**VS**\n{3}\n"
                                              "\n**멤버**\n{4} {5} {6} {7}\n{8} {9} {10} {11}\n"
                                              "\n**친선 인정 횟수**\n{12}번\n"
                                              "\n**기록 완료**\n".format(tMonth, tDate, tTime, '내전',
                                                                     member[0], member[1], member[2], member[3],
                                                                     member[4], member[5], member[6], member[7],
                                                                     tCount),

                                  color=0x62c1cc)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed)
        else:
            if url[0:26] == "https://cdn.discordapp.com":  # look to see if url is from discord
                embed = discord.Embed(title='🫰내전 임베드 ',
                                      description="\n\n**친선 시간**\n{0}월 {1}일 {2}시\n"
                                                  "\n**VS**\n{3}\n"
                                                  "\n**멤버**\n{4} {5} {6} {7}\n{8} {9} {10} {11}\n"
                                                  "\n**친선 인정 횟수**\n{12}번\n"
                                                  "\n**기록 완료**\n".format(tMonth, tDate, tTime, '내전',
                                                                         member[0], member[1], member[2], member[3],
                                                                         member[4], member[5], member[6], member[7],
                                                                         tCount),
                                      color=0x62c1cc)
                embed.set_image(url=url)
                await ctx.message.delete()
                await ctx.channel.send(embed=embed)


@bot.command()
async def 횟수(ctx):
    id = ctx.message.author.id

    file_path = "data.json"

    with open(file_path) as f:
        df = json.load(f)

    if df.get('{0}'.format(id)) == None:
        await ctx.channel.send("등록되어 있지 않은 사용자입니다!")
    else:
        await ctx.channel.send(
            "{0}님의 이번달 친선 횟수 : {1}".format(ctx.message.author.mention, df.get('{0}'.format(id))['cnt']))


@bot.command()
async def 이번달(ctx):
    id = ctx.message.author.id
    guild = ctx.message.guild
    member = guild.get_member(id)

    permission = 0

    try:
        for role in member.roles:
            if permission < role.position:
                permission = role.position

    except:
        pass

    file_path = "data.json"

    if permission >= 9 or guild.owner_id == id:
        with open(file_path) as f:
            df = json.load(f)
            for index, (key, elem) in enumerate(df.items()):
                await ctx.channel.send("{0} :  {1}".format(elem['nickname'], (elem['cnt'])))
    else:
        await ctx.channel.send(f"{ctx.message.author.mention}님은 권한이 없습니다!")


@bot.command()
async def 포인트(ctx):
    id = ctx.message.author.id
    guild = ctx.message.guild
    member = guild.get_member(id)

    permission = 0

    try:
        for role in member.roles:
            if permission < role.position:
                permission = role.position

    except:
        pass

    file_path = "three_month_data.json"

    if permission >= 9 or guild.owner_id == id:
        with open(file_path) as f:
            df = json.load(f)
            for index, (key, elem) in enumerate(df.items()):
                await ctx.channel.send(
                    "{0} :  친선 횟수 : {1}  내전 횟수 : {2}".format(elem['nickname'], (elem['cnt']), (elem['our'])))
    else:
        await ctx.channel.send(f"{ctx.message.author.mention}님은 권한이 없습니다!")


@bot.command()
async def 닉변(ctx, input):
    id = ctx.message.author.id
    nick = ctx.message.author.nick
    if not nick:
        nick = ctx.message.author.name

    file_path = "data.json"
    file_path3 = "three_month_data.json"

    with open(file_path) as f:
        df = json.load(f)

    with open(file_path3) as f:
        df2 = json.load(f)

    if df.get('{0}'.format(id)) == None:
        await ctx.channel.send("등록되어 있지 않은 사용자입니다!")
    else:
        df.get('{0}'.format(id))['nickname'] = input
        df2.get('{0}'.format(id))['nickname'] = input

        await ctx.message.delete()
        await ctx.channel.send("{0}의 닉네임이 {1}(으)로 변경되었습니다.".format(ctx.message.author.mention, input))

    with open(file_path, 'w') as f:
        json.dump(df, f, indent=2, ensure_ascii=False)

    with open(file_path3, 'w') as f:
        json.dump(df2, f, indent=2, ensure_ascii=False)


@bot.command()
async def 초기화(ctx):
    id = ctx.message.author.id
    guild = ctx.message.guild

    file_path = "data.json"
    destination = "last_month_data.json"

    record_path = "Record.json"
    destination2 = "last_month_record.json"

    if guild.owner_id == id:
        with open(file_path) as f:
            df = json.load(f)

        with open(record_path) as f:
            df2 = json.load(f)

        shutil.copy2(file_path, destination)

        for index, (key, elem) in enumerate(df.items()):
            elem['cnt'] = 0

        with open(file_path, 'w') as f:
            json.dump(df, f, indent=2, ensure_ascii=False)

        await ctx.channel.send("유저 친선 횟수 초기화")

        with open(destination2, 'w') as f:
            json.dump(df2, f, indent=2, ensure_ascii=False)

        with open(record_path, 'w') as f:
            json.dump({}, f, indent=2, ensure_ascii=False)

        await ctx.channel.send("한달 기록 초기화")


    else:
        await ctx.channel.send(f"{ctx.message.author.mention}님은 권한이 없습니다!")


@bot.command()
async def 도움말(ctx):
    embed = discord.Embed(title='학봇 사용 설명서',
                          description="**등록**\n사용자 등록을 할 수 있습니다.\n`~등록`\n"
                                      "\n\n**친선기록**\n친선 횟수를 인정 받을 수 있습니다.\n `~친선기록 <월> <일> <시> <vs 상대팀> \n <@팀원1> <@팀원2> <@팀원3> <@팀원4>`\n `친선 참여자 디스코드 멘션 or 닉네임 작성\n 용병 껴서 친선 진행시 학크루 크루원만 입력`\n\n`입력 예시 1) ~친선기록 2월 01일 23시 vs 은하수 @야도란 @상빈 @이코2 @공수`\n"
                                      "\n\n**내전**\n내전 횟수를 인정 받을 수 있습니다.\n `~내전 <월> <일> <시> \n <@팀원1> <@팀원2> <@팀원3> <@팀원4> <@팀원5> <@팀원6> <@팀원7> <@팀원8> \n<친선 인정 횟수>`\n `내전 참여자 디스코드 멘션 or 닉네임 작성`\n"
                                      "\n\n**횟수**\n사용자의 이번달 친선 횟수를 확인할 수 있습니다.\n`~횟수`\n"
                                      "\n\n**닉변**\n친선 횟수 등록에 필요한 닉네임을 수정합니다.\n`~닉변 <닉네임>`\n"
                                      "\n\n**이번달**\n크루원 전원의 이번달 친선 횟수를 확인할 수 있습니다.\n`운영진 이상만 사용 가능합니다.`\n`~이번달`\n\n",
                          color=0x62c1cc)
    # embed.set_thumbnail(url= "https://cdn.discordapp.com/attachments/1061134921034383460/1067346756003696720/KakaoTalk_Photo_2023-01-24-16-34-33.gif")
    embed.set_footer(text='\n- 기타 질문은 모두 서동원#5533(온라인일 때만 가능)에게 DM 바랍니다')
    await ctx.channel.send(embed=embed)


@bot.command()
async def qnaglfakdmfEpdh(ctx):
    embed = discord.Embed()
    embed.set_image(url="https://cdn.discordapp.com/attachments/1061134921034383460/1070244729926733874/IMG_2025.png")
    await ctx.channel.send(embed=embed)


@bot.command()
async def zhfhskaktmzmEpdh(ctx):
    embed = discord.Embed()
    embed.set_image(url="https://cdn.discordapp.com/attachments/1061134921034383460/1070246428720513105/IMG_2023.png")
    await ctx.channel.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"해당하는 명령어가 없습니다! 바보{ctx.message.author.mention}!")


bot.run(token)
