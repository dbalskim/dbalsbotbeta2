import discord
import random
import os
import requests
from bs4 import BeautifulSoup

client = discord.Client()

emogilist = ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟')

@client.event
async def on_ready():
    print(client.user.id)
    print("ready")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/도움말"))


@client.event
async def on_message(message):
    if (message.content.startswith("하이 드발스") or message.content.startswith("하이드발스")):
        await message.channel.send("네")



    if message.content.startswith("/투표"):
        message_split = message.content.split()

        if ((len(message_split)) > 3 and (len(message_split)) <= 12):
            embed = discord.Embed(title="**[:loudspeaker:투표] " + message_split[1] + "**", description=":small_orange_diamond:아래에서 원하시는 항목을 투표해주세요", color=0x1ca54d)
            vote = message_split[2:]

            for i in range(len(vote)):
                embed.add_field(name=emogilist[i], value=vote[i], inline=False)

            message = await message.channel.send(embed=embed)

            for i in range(len(vote)):
                await message.add_reaction(emogilist[i])

        elif ((len(message_split)) > 12):
            embed = discord.Embed(title="드발스봇", description=":warning:투표 기능은 10개 항목까지만 지원합니다. 각 항목은 띄어쓰기 없이 작성해 주세요.", color=0x1ca54d)
            embed.add_field(name="사용법", value="/투표 투표주제 항목1 항목2 ⋯")
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="드발스봇", description=":warning:투표 항목은 2개 이상부터 가능합니다.", color=0x1ca54d)
            embed.add_field(name=":small_orange_diamond:사용법", value="/투표 투표주제 항목1 항목2 ⋯")
            await message.channel.send(embed=embed)




    if message.content.startswith("/팀 뽑기 "):
        blueEmbed = discord.Embed(title="블루팀", description="블루팀 멤버", color=0x3c7ed9) #블루팀 embed생성
        redEmbed = discord.Embed(title="레드팀", description="레드팀 멤버", color=0xe44530) #레드팀 embed생성
        blueMembers = 0 #블루팀 인원수 체크용
        redMembers = 0 #레드팀 인원수 체크용

        message_split = message.content.split() #띄어쓰기를 기준으로 문자열 쪼개기
        members = message_split[2:] #이름만 가져오기 위해 2번째 인덱스부터 추출

        for member in members: #멤버 수 만큼 반복
            if(blueMembers >= int(len(members) // 2)): #블루팀 인원이 과반수 이상이라면 해당 멤버를 레드팀에 추가
                redEmbed.add_field(name="레드팀", value=member, inline=True)
                redMembers += 1 #레드팀에 한 명이 추가됐다고 기록

            elif(redMembers >= int(len(members) // 2)): #레드팀 인원이 과반수 이상이라면 해당 멤버를 블루팀에 추가
                blueEmbed.add_field(name="블루팀", value=member, inline=True)
                blueMembers += 1 #블루팀에 한 명이 추가됐다고 기록

            else: #만일 모두 아니라면
                team = random.randint(1, 3) #랜덤 함수를 통해 1 또는 2의 난수를 획득

                if(team == 1): #만일 1이면 블루팀에 추가
                    blueEmbed.add_field(name="블루팀", value=member, inline=True)
                    blueMembers += 1 #블루팀에 한 명이 추가됐다고 기록

                else: #아니라면 (2라면) 레드팀에 추가
                    redEmbed.add_field(name="레드팀", value=member, inline=True)
                    redMembers += 1 #레드팀에 한 명이 추가됐다고 기록

        await message.channel.send(embed=blueEmbed) #출력
        await message.channel.send(embed=redEmbed)



    if message.content.startswith("/실검"):
        embed = discord.Embed(title="드발스봇", description="네이버 실시간 검색어 1 ~ 10위입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://t1.daumcdn.net/cfile/tistory/99E493445C0D20A143")
        json = requests.get("https://www.naver.com/srchrank?frm=main").json()
        ranks = json.get("data")
        i = 1
        for r in ranks:
            if i >= 11:
                break
            else:
                keyword = r.get("keyword")
                embed.add_field(name=str(i)+"위", value=keyword, inline=False)
                i += 1
        await message.channel.send(embed=embed)


    if message.content.startswith("/전적"):
        try:
            tierImage = {'Unrank':'//opgg-static.akamaized.net/images/medals/default.png', 'Iron':'//opgg-static.akamaized.net/images/medals/iron_2.png?image=q_auto:best&v=1', 'Bronze':'//opgg-static.akamaized.net/images/medals/bronze_4.png?image=q_auto:best&v=1',
                             'Silver':'//opgg-static.akamaized.net/images/medals/silver_2.png?image=q_auto:best&v=1', 'Gold':'//opgg-static.akamaized.net/images/medals/gold_2.png?image=q_auto:best&v=1',
                             'Platinum':'//opgg-static.akamaized.net/images/medals/platinum_2.png?image=q_auto:best&v=1', 'Diamond':'//opgg-static.akamaized.net/images/medals/diamond_1.png?image=q_auto:best&v=1',
                             'Master':'//opgg-static.akamaized.net/images/medals/master_1.png?image=q_auto:best&v=1', 'Grandmaster':'//opgg-static.akamaized.net/images/medals/grandmaster_1.png?image=q_auto:best&v=1',
                             'Challenger':'//opgg-static.akamaized.net/images/medals/challenger_1.png?image=q_auto:best&v=1'}
            tiers = ('Unrank', 'Iron', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master', 'Grandmaster', 'Challenger')
            message_split = message.content.split()
            name = ''.join(message_split[1:])
            embed = discord.Embed(title="드발스봇", description="다음은 " + name + "님의 op.gg 검색 결과입니다.", color=0x1ca54d)

            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
            url = 'https://www.op.gg/summoner/userName=' + name

            res = requests.get(url, headers = headers)

            soup = BeautifulSoup(res.content, 'html.parser')

            nick = soup.select('span.Name')
            team = str(soup.select('div.Team')[0].text).split()[0]

            

            if len(nick) == 2:
                embed.add_field(name=team + " " + nick[0].text, value=nick[1].text, inline=True)
            else:
                embed.add_field(name="이름", value=nick[0].text, inline=True)
            
            level = soup.select('span')[40].text
            embed.add_field(name="레벨", value=level, inline=True)

            ranking = soup.select('a')[47].text

            if "Ladder Rank" in ranking:
                ranking = ranking.split()
                embed.add_field(name="래더 랭킹", value=ranking[2] + "위 (상위 " + str(ranking[3])[1:-1] + "프로)", inline=True)

            soloRank = str(soup.select('div.TierRank'))
            if 'Unranked' in soloRank:
                embed.add_field(name="솔랭:dagger:", value=soloRank[32:-7], inline=False)
            else:
                embed.add_field(name="솔랭:dagger:", value=soloRank[23:-7], inline=False)
            for t in tiers:
                if t in soloRank:
                    embed.set_thumbnail(url="https:" + tierImage[t])

            freeRank = str(soup.select('div.sub-tier__rank-tier '))
            if 'Unranked' in freeRank:
                embed.add_field(name="자랭:crossed_swords:", value=freeRank[43:-7], inline=False)
            else:
                embed.add_field(name="자랭:crossed_swords:", value=freeRank[35:-7], inline=False)

            mostChamp = str(soup.select('div.ChampionName')[0].text)
            embed.add_field(name="가장 많이 플레이한 챔피언", value=mostChamp, inline=True)
            games = str(soup.select('div.Title')[0].text)

            embed.add_field(name="횟수", value=games[0:-7] + " games", inline=True)

            winRate = str(soup.select('div.WinRatioGraph')[-1].text)
            embed.add_field(name="승률", value=winRate, inline=False)



            
            

            embed.add_field(name="자세한 정보는 op.gg에서 확인하세요", value='https://www.op.gg/summoner/userName=' + name, inline=False)


            await message.channel.send(embed=embed)

        except:
            embed = discord.Embed(title="드발스봇", description=":warning:해당 소환사의 전적이 존재하지 않습니다.", color=0x1ca54d)
            embed.add_field(name=":small_orange_diamond:사용법", value="/전적 소환사닉네임")
            await message.channel.send(embed=embed)



    if message.content.startswith("/날씨"):
        try:
            message_split = message.content.split()
            if(len(message_split) == 1):
                loc = "부평"
            else:
                loc = str(message_split[1:])[2:-2]

            embed = discord.Embed(title="드발스봇", description="다음은 " + loc + "의 날씨입니다:sunrise_over_mountains:", color=0x1ca54d)

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
            url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=' + loc + "날씨"

            res = requests.get(url, headers=headers)

            soup = BeautifulSoup(res.content, 'html.parser')

            todaytemp = str(soup.select('span.todaytemp')[0].text) + "℃"
            cast = str(soup.select('p.cast_txt')[0].text)


            embed.add_field(name=todaytemp + ":thermometer:", value=cast, inline=False)

            sensible = str(soup.select('span.num')[2].text)

            embed.add_field(name="체감 온도", value=sensible, inline=False)

            await message.channel.send(embed=embed)

        except:
            embed = discord.Embed(title="드발스봇", description=":warning:해당 지역의 날씨 정보가 존재하지 않습니다.", color=0x1ca54d)
            embed.add_field(name=":small_orange_diamond:사용법", value="/날씨 [지역]")
            await message.channel.send(embed=embed)


    if message.content.startswith("/코로나"):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')

        embed = discord.Embed(title="드발스봇", description="국내 코로나 현황입니다:microbe:", color=0x1ca54d)

        patients = str(soup.select('p.info_num')[0].text)
        inspection = str(soup.select('p.info_num')[1].text)
        Quarantine = str(soup.select('p.info_num')[2].text)
        dead = str(soup.select('p.info_num')[3].text)
        domesticNewPatients = str(soup.select('em.info_num')[0].text)
        overseasNewPatients = str(soup.select('em.info_num')[1].text)

        newPatients = int(domesticNewPatients) + int(overseasNewPatients)


        embed.add_field(name="확진환자", value=patients, inline=True)
        embed.add_field(name="검사 중", value=inspection, inline=True)
        embed.add_field(name="격리 해제", value=Quarantine, inline=True)
        embed.add_field(name="사망자", value=dead, inline=True)
        embed.add_field(name="신규 확진자", value=newPatients, inline=True)

        await message.channel.send(embed=embed)

    


    if message.content.startswith("/챔피언"):
        try:
            message_split = message.content.split()
            champ = str(message_split[1:])[2:-2]

            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
            url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%A6%AC%EA%B7%B8+%EC%98%A4%EB%B8%8C+%EB%A0%88%EC%A0%84%EB%93%9C+' + champ
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.content, 'html.parser')

            embed = discord.Embed(title="드발스봇", description="다음은 " + champ + "에 관한 정보입니다", color=0x1ca54d)


            champImgUrl = soup.findAll("div",class_="area_img_box")
            champImg = str(champImgUrl).split('src="')[1][:-23]
            embed.set_thumbnail(url=champImg)

            champName = str((soup.select('span.text'))).split("</strong>")[0][28:]
            embed.add_field(name="이름", value=champName, inline=True)

            champRole = str(soup.select('div.info_group')[1]).split("<dd>")[1][1:-12]
            embed.add_field(name="역할", value=champRole, inline=True)

            champloc = str(soup.select('div.info_group')[2]).split("<dd>")[1][1:-12]
            embed.add_field(name="지역", value=champloc, inline=True)

            if champ == "아트록스" or champ == "그레이브즈":
                champDesc = str(soup.select('span')[72]).split('<br/>')
                champDescs = ""

            else:
                champDesc = str(soup.select('span')[70]).split('<br/>')
                champDescs = ""
            for i in range(1, len(champDesc)):
                champDescs = champDescs + champDesc[i]
            embed.add_field(name=champDesc[0][25:], value=champDescs[:-7], inline=True)

            await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="드발스봇", description=":warning:해당 챔피언의 정보가 존재하지 않습니다.", color=0x1ca54d)
            embed.add_field(name=":small_orange_diamond:사용법", value="/챔피언 [챔피언이름]")
            await message.channel.send(embed=embed)



    if message.content.startswith("/핑"):
        embed = discord.Embed(title="드발스봇", description="핑: {}ms".format(client.latency), color=0x1ca54d)
        await message.channel.send(embed=embed)

    

    if (message.content.startswith("/소환사의 협곡") or message.content.startswith("/소환사의협곡")):
        embed = discord.Embed(title="드발스봇", description="다음은 소환사의 협곡에 관한 정보입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://dbscthumb-phinf.pstatic.net/5108_000_1/20191227164428754_3FKN0L9OP.png/14%EB%A1%A4.png?type=m1500_q100")

        embed.add_field(name="소환사의 협곡", value="""리그 오브 레전드의 대표적 전장인 소환사의 협곡은 가장 많은 플레이어들이 선호하는 전장입니다. 각 다섯 명의 챔피언으로 두 팀을 구성하여, 세 갈래 공격로와 넓은 정글을 오가며 교전을 펼치게 됩니다. 
        
정글에는 강력한 효과를 부여해 주는 중립 몬스터들이 포진해 있습니다. 공격로 대치 단계가 길고, 대규모 팀간 전투가 벌어지는 것이 가장 큰 특징입니다.""", inline=False)
        embed.set_image(url="https://dbscthumb-phinf.pstatic.net/5108_000_1/20191227163621540_GRQ7G0TFQ.jpg/0%EB%A1%A41.jpg?type=m1500_q100")

        embed.add_field(name="""<기본 정보>
방어와 파괴""", value="""많은 소환사 여러분께 사랑받는 소환사의 협곡은 치열한 경쟁이 벌어지는 리그 오브 레전드의 대표적 맵이며, 프로 경기가 펼쳐지는 전장이기도 합니다.

협곡에서의 전투는 공격로 상대와 벌이는 소규모 교전으로 시작해 손에 땀을 쥐게 하는 대규모 팀 전투로 발전해 갑니다. 상대 팀의 기지를 향해 공격로를 압박해 들어가 적의 넥서스를 파괴하고 승리를 차지하세요.""", inline=False)
        embed.add_field(name="협곡의 전투", value="""가장 넓은 전장인 소환사의 협곡은 대각선을 기준으로 대칭을 이루고 있으며, 적의 기지까지 세 개의 공격로가 배치되어 있습니다. 공격로마다 각각 세 개의 포탑과 하나의 억제기가 방어하고 있으며, 넥서스는 두 개의 포탑이 지키고 있습니다.
        
양 팀 진영에는 강력한 효과를 제공하는 넓은 정글이 있고, 중앙을 가로지르는 강에는 팀 전체에 이로운 효과를 주는 에픽 몬스터 둘이 자리 잡고 있습니다.""", inline=False)
        embed.add_field(name="""<맵 정보>
중립지역 (내셔 남작)""", value="""상단 공격로 근처의 강에는 이 무시무시한 에픽 몬스터의 둥지가 있습니다. 리그 오브 레전드에서 가장 강력한 중립 몬스터인 내셔 남작은 잘 성장한 챔피언들에게도 쉽지 않은 상대입니다. 내셔 남작을 처치하면 생존한 모든 아군 챔피언에게 남작의 도움 효과가 적용됩니다. 

* 남작의 도움 : 공격력과 주문력이 크게 상승하며, 귀환 시간을 상당히 줄여줍니다. 주위의 모든 미니언에게도 사거리, 피해량, 이동 속도, 입는 피해 감소 등의 강력한 효과가 적용됩니다.""", inline=False)
        embed.add_field(name="중립지역 (드래곤)", value="""하단 공격로 근처의 강에 자리잡은 이 에픽 몬스터는 보통 여러 명이 함께 공격하는 것이 좋습니다. 드래곤을 처치하면 팀원 전체가 영구히 중첩되는 드래곤 사냥꾼 효과를 얻을 수 있습니다. 드래곤 사냥꾼 중첩이 더 높은 팀에게는 드래곤이 추가 피해를 입히며, 피해를 덜 받습니다.

* 1회 처치 – 드래곤의 힘 : 공격력과 주문력이 상승합니다.
* 2회 처치 – 드래곤의 분노 : 포탑과 구조물에 입히는 피해량이 증가합니다.
* 3회 처치 – 드래곤의 날개 : 이동 속도가 상승합니다.
* 4회 처치 – 드래곤의 지배 : 미니언과 몬스터에게 입히는 피해량이 증가합니다.
* 5회 처치 – 드래곤의 위상 : 드래곤 사냥꾼의 모든 추가 효과가 두 배로 적용되며 적을 공격하면 큰 지속 피해를 추가로 입힙니다.""", inline=False)
        embed.add_field(name="중립지역 (정글)", value="""소환사의 협곡에 대칭으로 자리잡은 정글 지역에는 강타 소환사 주문을 사용하면 각기 독특한 효과를 제공하는 하급 몬스터 캠프들뿐만 아니라, 처치할 경우 더 강력하며 오래 가는 효과를 얻을 수 있는 강력한 몬스터 캠프가 둘씩 있습니다.

정글 몬스터에게 얻은 효과를 잘 관리해야 전장에서 최고의 활약을 펼칠 수 있으므로 아군 정글에 적이 침입하진 않는지 잘 살피셔야 합니다. 이로운 효과를 빼앗길 수 있으니까요!

* 잉걸불의 문장 : 붉은 덩굴정령을 처치하면 일시적으로 잉걸불의 문장 효과를 얻어, 기본 공격으로 적에게 둔화를 걸고 지속 피해를 입히며, 일정 시간 동안 체력을 회복합니다.
* 통찰력의 문장 : 푸른 파수꾼을 처치하면 일시적으로 통찰력의 문장 효과를 얻어, 스킬 재사용 대기시간이 줄어들고 마나 회복 속도가 높아집니다.""", inline=False)

        await message.channel.send(embed=embed)


    if (message.content.startswith("/칼바람 나락") or message.content.startswith("/칼바람나락")):
        embed = discord.Embed(title="드발스봇", description="다음은 칼바람 나락에 관한 정보입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://dbscthumb-phinf.pstatic.net/5108_000_1/20191227171425036_A0TVWS3I9.png/15%EB%A1%A4.png?type=m1500_q100")
        embed.set_image(url="https://dbscthumb-phinf.pstatic.net/5108_000_1/20191227172324554_KNKM12YW3.jpg/0%EB%A1%A410.jpg?type=m1500_q100")

        embed.add_field(name="칼바람 나락", value="""칼바람 나락은 프렐요드에서도 가장 춥고 척박한 땅에 자리잡은, 바닥을 가늠할 수 없는 협곡입니다. 아주 먼 옛날, 이 깎아지른 골짜기에 놓인 좁은 다리위에서 격전이 벌어졌었다는 전설이 있습니다.

누가, 어떤 이유로 이 곳에서 싸웠는지는 전해지지 않지만, 지금도 귀를 기울이면 협곡 아래로 내던져진 패배자들의 비명소리가 칼바람에 실려 들려온다고들 합니다.""", inline=False)
        embed.add_field(name="""<기본 정보>
나락 전투""", value="""리그 오브 레전드에서 유일한 단일 공격로 전장인 칼바람 나락은 다리의 양 끝에 각 팀의 기지가 있습니다. 다리에는 팀 별로 두 개의 포탑과 억제기가 있으며, 넥서스는 두 개의 포탑이 방어합니다.

잠시도 숨 돌릴 중립 지대가 없는 칼바람 나락은 다른 어떤 맵보다 팀간 전투가 더욱 빈번하고 치열하게 벌어집니다.""", inline=False)
        embed.add_field(name="방어와 파괴", value="""플레이어 여러분이 고안한 이 모드는 이제 리그 오브 레전드에서 가장 인기 있는 게임 모드 중 하나로 자리 잡았습니다. 칼바람 나락은 중립 지역이 없고, 하나의 공격로에서 다섯 명의 챔피언으로 구성된 두 팀이 전투를 벌이게 됩니다.

각 챔피언은 많은 골드를 가지고 3레벨로 시작하여, 처음부터 아슬아슬하고 치열한 대규모 팀 전투로 뛰어듭니다.""", inline=False)
        embed.add_field(name="""<쉼 없는 전투>
체력 회복과 상점 이용 불가""", value="""칼바람 나락에서는 소환사의 제단으로 가도 체력이 회복되지 않으며, 아이템 구매 역시 불가능합니다. 챔피언은 전장에서 죽었을 때만 아이템을 구매할 수 있습니다. 귀환 주문 또한 이 게임 모드에서는 사용할 수 없습니다.""", inline=False)
        embed.add_field(name="체력의 유물", value="""체력을 회복할 소환사의 제단이 없기 때문에, 다리 곳곳에 일정한 간격으로 체력의 유물이 배치되어 있습니다. 이 유물을 차지하면 짧은 시간 동안 챔피언의 체력과 마나가 빠르게 회복됩니다.""", inline=False)
        embed.add_field(name="한 개의 억제기", value="""공격로가 하나이기 때문에, 단 하나의 억제기가 게임의 승패를 가르게 됩니다. 억제기가 파괴되면 적 팀은 즉시 미니언 무리에 슈퍼 미니언이 추가 소환됩니다. 억제기만은 목숨을 걸고라도 반드시 방어해야 합니다.""", inline=False)
        
        await message.channel.send(embed=embed)


    if message.content.startswith("/강타"):
        embed = discord.Embed(title="드발스봇", description="다음은 강타에 관한 정보입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://s.pstatic.net/dbscthumb.phinf/5104_000_1/20171208010529143_QR7OJI6A7.png/lol_spell_smite.png?type=m1500_q100")
        embed.add_field(name="게임 모드", value="소환사의 협곡", inline=False)
        embed.add_field(name="재사용대기시간", value="90초", inline=False)
        embed.set_footer(text="""* 적 미니언이나 소환수에게 390-1000 (챔피언 레벨에 따라 변동) 의 고정 피해를 입힙니다. 몬스터에게 사용 시 체력도 70 + (최대 체력의 10%)만큼 회복합니다.

* 강타는 90초에 한 번씩 충전되며, 최대 2회까지 충전됩니다. 해당 주문을 한 번 사용한 후, 재사용 대기시간 15초가 적용됩니다.""")
        await message.channel.send(embed=embed)

    if message.content.startswith("/방어막") or message.content.startswith("/배리어") or message.content.startswith("/보호막"):
        embed = discord.Embed(title="드발스봇", description="다음은 방어막에 관한 정보입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://s.pstatic.net/dbscthumb.phinf/5104_000_1/20171130113146137_QI8GRUQKW.png/lol_spell_barrie.png?type=m1500_q100")
        embed.add_field(name="게임 모드", value="소환사의 협곡, 칼바람 나락", inline=False)
        embed.add_field(name="재사용대기시간", value="180초", inline=False)
        embed.set_footer(text="""* 2초 동안 방어막으로 감싸 피해를 115-455(챔피언 레벨에 따라 변동)만큼 흡수합니다.""")
        await message.channel.send(embed=embed)

    if message.content.startswith("/순간이동") or message.content.startswith("/텔") or message.content.startswith("/텔레포트") or message.content.startswith("/텔포"):
        embed = discord.Embed(title="드발스봇", description="다음은 순간이동에 관한 정보입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://s.pstatic.net/dbscthumb.phinf/5104_000_1/20171130113102375_PXNN1SDTP.png/lol_spell_telepo.png?type=m1500_q100")
        embed.add_field(name="게임 모드", value="소환사의 협곡", inline=False)
        embed.add_field(name="재사용대기시간", value="360초", inline=False)
        embed.set_footer(text="""* 4초 동안 정신을 집중한 다음, 챔피언이 지정한 아군 구조물, 미니언, 혹은 와드로 순간이동합니다.""")
        await message.channel.send(embed=embed)

    if message.content.startswith("/유체화"):
        embed = discord.Embed(title="드발스봇", description="다음은 유체화에 관한 정보입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://s.pstatic.net/dbscthumb.phinf/5104_000_1/20171208010528099_TD5DODV5A.png/lol_spell_ghost.png?type=m1500_q100")
        embed.add_field(name="게임 모드", value="소환사의 협곡, 칼바람 나락", inline=False)
        embed.add_field(name="재사용대기시간", value="210초", inline=False)
        embed.set_footer(text="""* 챔피언이 10초 동안 유닛과 충돌하지 않게 되며 이동 속도가 상승합니다. 이동 속도는 레벨에 따라 최대 24~48%까지 상승합니다. 유체화 사용 후 적을 처치하면 이동 속도 증가 효과 지속시간이 4~7초 증가합니다.""")
        await message.channel.send(embed=embed)

    if message.content.startswith("/점멸") or message.content.startswith("/플") or message.content.startswith("/플래쉬"):
        embed = discord.Embed(title="드발스봇", description="다음은 점멸에 관한 정보입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://s.pstatic.net/dbscthumb.phinf/5104_000_1/20171130113103900_18QJAE1MN.png/lol_spell_flash.png?type=m1500_q100")
        embed.add_field(name="게임 모드", value="소환사의 협곡, 칼바람 나락", inline=False)
        embed.add_field(name="재사용대기시간", value="300초", inline=False)
        embed.set_footer(text="""* 커서가 가리키는 방향으로 챔피언을 순간이동시킵니다.""")
        await message.channel.send(embed=embed)

    if message.content.startswith("/점화"):
        embed = discord.Embed(title="드발스봇", description="다음은 점화에 관한 정보입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://s.pstatic.net/dbscthumb.phinf/5104_000_1/20171130113103883_I5C6H4ZD2.png/lol_spell_ignite.png?type=m1500_q100")
        embed.add_field(name="게임 모드", value="소환사의 협곡, 칼바람 나락", inline=False)
        embed.add_field(name="재사용대기시간", value="180초", inline=False)
        embed.set_footer(text="""* 대상 적 챔피언을 불태워, 5초에 걸쳐 70~410(챔피언 레벨에 따라 변동)의 고정 피해를 입히고 그동안 적의 위치를 드러내며 고통스러운 상처를 적용합니다.

* 고통스러운 상처는 회복 효과를 40% 감소시킵니다. 또한, 은신 중인 적은 위치가 드러나지 않습니다.""")
        await message.channel.send(embed=embed)

    if message.content.startswith("/정화"):
        embed = discord.Embed(title="드발스봇", description="다음은 정화에 관한 정보입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://s.pstatic.net/dbscthumb.phinf/5104_000_1/20171130113102609_8P1LXPHX5.png/lol_spell_cleans.png?type=m1500_q100")
        embed.add_field(name="게임 모드", value="소환사의 협곡, 칼바람 나락", inline=False)
        embed.add_field(name="재사용대기시간", value="210초", inline=False)
        embed.set_footer(text="""* 챔피언에 걸린 모든 이동 불가(제압, 에어본 제외)와 소환사 주문에 의한 해로운 효과를 제거하고 새로 적용되는 이동 불가 효과들의 지속 시간을 3초간 65%로 감소시킵니다.""")
        await message.channel.send(embed=embed)

    if message.content.startswith("/총명"):
        embed = discord.Embed(title="드발스봇", description="다음은 총명에 관한 정보입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://s.pstatic.net/dbscthumb.phinf/5104_000_1/20171208010529816_J37DV3W14.png/lol_spell_clarit.png?type=m1500_q100")
        embed.add_field(name="게임 모드", value="칼바람 나락", inline=False)
        embed.add_field(name="재사용대기시간", value="144초", inline=False)
        embed.set_footer(text="""* 챔피언의 최대 마나량의 50%, 주변 아군의 최대 마나가 25% 만큼 회복됩니다.""")
        await message.channel.send(embed=embed)

    if message.content.startswith("/탈진"):
        embed = discord.Embed(title="드발스봇", description="다음은 탈진에 관한 정보입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://s.pstatic.net/dbscthumb.phinf/5104_000_1/20171208010528094_JHFI7SK8O.png/lol_spell_exhaus.png?type=m1500_q100")
        embed.add_field(name="게임 모드", value="소환사의 협곡, 칼바람 나락", inline=False)
        embed.add_field(name="재사용대기시간", value="210초", inline=False)
        embed.set_footer(text="""* 적 챔피언을 지치게 만들어 3초 동안 이동 속도를 30% 낮추며, 이 동안 가하는 피해량을 40% 낮춥니다.""")
        await message.channel.send(embed=embed)

    if message.content.startswith("/회복") or message.content.startswith("/힐"):
        embed = discord.Embed(title="드발스봇", description="다음은 회복에 관한 정보입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://s.pstatic.net/dbscthumb.phinf/5104_000_1/20171208010528629_WOV604M43.png/lol_spell_heal.png?type=m1500_q100")
        embed.add_field(name="게임 모드", value="소환사의 협곡, 칼바람 나락", inline=False)
        embed.add_field(name="재사용대기시간", value="240초", inline=False)
        embed.set_footer(text="""* 챔피언과 대상 아군 챔피언의 체력을 90~345만큼 (챔피언 레벨에 따라 변동) 회복시키고 1초 동안 이동 속도가 30% 증가합니다. 최근 소환사 주문 회복의 영향을 받은 유닛의 경우 치유량이 절반만 적용됩니다.

* 이 주문은 대상을 정하지 않은 경우, 범위 내에서 가장 큰 부상을 입은 아군 챔피언에게 시전됩니다.""")
        await message.channel.send(embed=embed)

    if message.content.startswith("/표식"):
        embed = discord.Embed(title="드발스봇", description="다음은 표식 / 돌진에 관한 정보입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://s.pstatic.net/dbscthumb.phinf/5104_000_1/20171130113236520_05U9I47W1.png/lol_spell_mark.png?type=m1500_q100")
        embed.add_field(name="게임 모드", value="칼바람 나락", inline=False)
        embed.add_field(name="재사용대기시간", value="48초/3초", inline=False)
        embed.set_footer(text="""* 눈덩이를 던져 첫 번째 맞은 적에게 (10 + 레벨당 5)의 고정 피해를 입히고 대상에 대한 절대 시야를 얻습니다. 적을 맞히면 이 스킬을 3초 내에 재시전하여 표식이 남은 유닛에게 돌진하여 추가로 (10 + 레벨당 5)의 고정 피해를 입힙니다.

* 대상에게 돌진하면 표식의 재사용 대기시간이 25% 감소합니다.""")
        await message.channel.send(embed=embed)

    if message.content.startswith("/마인리스트"):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        url = 'https://minelist.kr/'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')

        embed = discord.Embed(title="드발스봇", description="다음은 마인리스트 서버 순위 1 ~ 5위입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://minelist.kr/assets/logo-ca99433b622254e68f0168fc72d260a7d8ed88f22f600dbe433a094e43b17c51.png")
        
        servers = soup.select('h4.server-title')
        server1 = str(servers[0]).split('</span>')[1]
        server2 = str(servers[1]).split('</span>')[1]
        server3 = str(servers[2]).split('</span>')[1]
        server4 = str(servers[3]).split('</span>')[1]
        server5 = str(servers[4]).split('</span>')[1]

        desc1 = soup.select('p.text-muted')[0].text
        desc2 = soup.select('p.text-muted')[1].text
        desc3 = soup.select('p.text-muted')[2].text
        desc4 = soup.select('p.text-muted')[3].text
        desc5 = soup.select('p.text-muted')[4].text

        embed.add_field(name="1위 : " + server1, value=desc1, inline=False)
        embed.add_field(name="2위 : " + server2, value=desc2, inline=False)
        embed.add_field(name="3위 : " + server3, value=desc3, inline=False)
        embed.add_field(name="4위 : " + server4, value=desc4, inline=False)
        embed.add_field(name="5위 : " + server5, value=desc5, inline=False)
        embed.add_field(name="자세한 정보는 마인리스트에서 확인하세요", value="https://minelist.kr/", inline=False)

        await message.channel.send(embed=embed)



    if message.content.startswith("/하픽"):
        try:
            message_split = message.content.split()
            name = message_split[1]

            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
            url = 'https://plancke.io/hypixel/player/stats/' + name
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.content, 'html.parser')

            embed = discord.Embed(title="드발스봇", description="다음은 " + name + "님의 하이픽셀 전적입니다.", color=0x1ca54d)
            embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/795149565871558660/egdzdzPd.jpg")

            nicks = str(soup.select('span')[11:-3]).split('</span>')
            nick = ""
            for i in range(len(nicks)):
                nick = nick + str(str(nicks[i]).split(">")[-1])

            nick = nick[:-1].strip()

            embed.add_field(name="이름", value=nick, inline=True)

            guild = soup.select('a')[22]
            if '/hypixel/guild/player/' in str(guild):
                guild = guild.text
                embed.add_field(name="길드", value=guild, inline=True)

            level = str(str(soup.select('div')[22]).split("Level:</b> ")[1]).split("<br/>")[0]
            
            embed.add_field(name="레벨", value=level, inline=True)

            karma = str(str(soup.select('div')[22]).split("Karma:</b> ")[1]).split("<br/>")[0]
            embed.add_field(name="카르마", value=karma, inline=True)

            skywars = soup.select('div.panel-body')[10]

            embed.add_field(name="<스카이워즈>", value="레벨 " + str(str(skywars).split("Level:</b> ")[1]).split("</li>")[0], inline=False)
            embed.add_field(name="티어", value=str(str(skywars).split("Prestige:</b> ")[1]).split("</li>")[0], inline=True)
            embed.add_field(name="승리", value=str(str(skywars).split("Wins:</b> ")[1]).split("</li>")[0], inline=True)
            embed.add_field(name="패배", value=str(str(skywars).split("Losses:</b> ")[1]).split("</li>")[0], inline=True)
            embed.add_field(name="킬", value=str(str(skywars).split("Kills:</b> ")[1]).split("</li>")[0], inline=True)
            embed.add_field(name="어시", value=str(str(skywars).split("Assists:</b> ")[1]).split("</li>")[0], inline=True)
            embed.add_field(name="데스", value=str(str(skywars).split("Deaths:</b> ")[1]).split("</li>")[0], inline=True)
            embed.add_field(name="킬뎃", value=str(str(skywars).split("Kill/Death Ratio:</b> ")[1]).split("</li>")[0], inline=True)

            bedwars = soup.select('div.panel-body')[3]
            bedwar = str(bedwars).split("<td>")

            embed.add_field(name="<배드워즈>", value="레벨 " + str(str(bedwars).split("Level:</b> ")[1]).split("</li>")[0], inline=False)
            embed.add_field(name="승리", value=str(bedwar[110]).split("</td>")[0], inline=True)
            embed.add_field(name="패배", value=str(bedwar[111]).split("</td>")[0], inline=True)
            embed.add_field(name="킬", value=str(bedwar[106]).split("</td>")[0], inline=True)
            embed.add_field(name="데스", value=str(bedwar[107]).split("</td>")[0], inline=True)
            embed.add_field(name="킬뎃", value=str(str(bedwar[107]).split('#f3f3f3">')[1]).split("</td>")[0], inline=True)
            embed.add_field(name="파킬", value=str(bedwar[108]).split("</td>")[0], inline=True)
            embed.add_field(name="파뎃", value=str(bedwar[109]).split("</td>")[0], inline=True)
            embed.add_field(name="침대 파괴", value=str(bedwar[112]).split("</td>")[0], inline=True)
        
        except:
            embed = discord.Embed(title="드발스봇", description=":warning:해당 플레이어의 전적이 존재하지 않습니다.", color=0x1ca54d)
            embed.add_field(name=":small_orange_diamond:사용법", value="/하픽 플레이어닉네임")

        finally:
            await message.channel.send(embed=embed)















    if message.content.startswith("/도움말"):
        embed = discord.Embed(title="드발스봇", description=":small_orange_diamond:드발스봇을 이용해주셔서 감사합니다", color=0x1ca54d)
        embed.add_field(name=":small_blue_diamond:호출", value="하이 드발스", inline=False)
        embed.add_field(name=":small_blue_diamond:투표", value="/투표 [투표주제] [항목1] [항목2] ⋯", inline=False)
        embed.add_field(name=":small_blue_diamond:팀 뽑기", value="/팀 뽑기 [이름] [이름] ⋯", inline=False)
        embed.add_field(name=":small_blue_diamond:네이버 실시간 검색어 확인", value="/실검", inline=False)
        embed.add_field(name=":small_blue_diamond:롤 전적 검색", value="/전적 [소환사닉네임]", inline=False)
        embed.add_field(name=":small_blue_diamond:날씨 확인", value="/날씨 [지역]", inline=False)
        embed.add_field(name=":small_blue_diamond:코로나 현황 확인", value="/코로나", inline=False)
        embed.add_field(name=":small_blue_diamond:챔피언 정보 확인", value="/챔피언 [챔피언이름]", inline=False)
        embed.add_field(name=":small_blue_diamond:드발스봇 핑 정보", value="/핑", inline=False)
        embed.add_field(name=":small_blue_diamond:롤 게임모드 정보", value="/소환사의 협곡 또는 /칼바람 나락", inline=False)
        embed.add_field(name=":small_blue_diamond:롤 소환사 주문 정보", value="/[소환사 주문]", inline=False)
        embed.add_field(name=":small_blue_diamond:마인리스트 서버 순위", value="/마인리스트", inline=False)
        embed.add_field(name=":small_blue_diamond:하이픽셀 플레이어 정보", value="/하픽 [플레이어닉네임]", inline=False)

        
        await message.channel.send(embed=embed)



access_token = os.environ['BOT_TOKEN']
client.run(access_token)
