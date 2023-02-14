from .config import petpet_config
from .functions import *

memes = [
    Meme("universal", universal, ("万能表情", "空白表情")),
    Meme("petpet", petpet, ("摸", "摸摸", "摸头", "rua"), r"摸摸?头?|rua"),
    Meme("kiss", kiss, ("亲", "亲亲"), r"亲亲?"),
    Meme("rub", rub, ("贴", "贴贴", "蹭", "蹭蹭"), r"贴贴?|蹭蹭?"),
    Meme("capoo_rub", capoo_rub, ("咖波蹭",)),
    Meme("play", play, ("顶", "玩")),
    Meme("pat", pat, ("拍",)),
    Meme("rip", rip, ("撕",)),
    Meme("rip_angrily", rip_angrily, ("怒撕",)),
    Meme("throw", throw, ("丢", "扔")),
    Meme("throw_gif", throw_gif, ("抛", "掷")),
    Meme("crawl", crawl, ("爬",)),
    Meme("support", support, ("精神支柱",)),
    Meme("always", always, ("一直",)),
    Meme("always_cycle", always_cycle, ("一直套娃",)),
    Meme("always_always", always_always, ("一直一直",)),
    Meme("loading", loading, ("加载中",)),
    Meme("turn", turn, ("转",)),
    Meme("windmill_turn", windmill_turn, ("风车转",)),
    Meme("littleangel", littleangel, ("小天使",)),
    Meme("dont_touch", dont_touch, ("不要靠近",)),
    Meme("alike", alike, ("一样",)),
    Meme("roll", roll, ("滚",)),
    Meme("play_game", play_game, ("玩游戏",), r"来?玩游戏"),
    Meme("worship", worship, ("膜", "膜拜"), r"膜拜?"),
    Meme("eat", eat, ("吃",)),
    Meme("klee_eat", klee_eat, ("可莉吃",)),
    Meme("bite", bite, ("啃",)),
    Meme("hutao_bite", hutao_bite, ("胡桃啃",)),
    Meme("police", police, ("出警",)),
    Meme("police1", police1, ("警察",)),
    Meme("ask", ask, ("问问",), r"去?问问"),
    Meme("prpr", prpr, ("舔", "舔屏", "prpr"), r"舔屏?|prpr"),
    Meme("twist", twist, ("搓",)),
    Meme("wallpaper", wallpaper, ("墙纸",)),
    Meme("china_flag", china_flag, ("国旗",)),
    Meme("make_friend", make_friend, ("交个朋友",)),
    Meme("back_to_work", back_to_work, ("继续干活", "打工人")),
    Meme("perfect", perfect, ("完美",), r"完美的?"),
    Meme("follow", follow, ("关注",)),
    Meme("my_friend", my_friend, ("我朋友说",), r"我(?:有个)?朋友(?P<name>.*?)说"),
    Meme("paint", paint, ("这像画吗",)),
    Meme("shock", shock, ("震惊",)),
    Meme("coupon", coupon, ("兑换券",)),
    Meme("listen_music", listen_music, ("听音乐",)),
    Meme("dianzhongdian", dianzhongdian, ("典中典", "黑白草图")),
    Meme("funny_mirror", funny_mirror, ("哈哈镜",)),
    Meme("love_you", love_you, ("永远爱你",)),
    Meme("symmetric", symmetric, ("对称",)),
    Meme("safe_sense", safe_sense, ("安全感",)),
    Meme("always_like", always_like, ("我永远喜欢",), r"我?永远喜欢"),
    Meme("interview", interview, ("采访",)),
    Meme("punch", punch, ("打拳",)),
    Meme("cyan", cyan, ("群青",)),
    Meme("pound", pound, ("捣",)),
    Meme("thump", thump, ("捶",)),
    Meme("need", need, ("需要", "你可能需要")),
    Meme("cover_face", cover_face, ("捂脸",)),
    Meme("knock", knock, ("敲",)),
    Meme("garbage", garbage, ("垃圾", "垃圾桶"), r"垃圾桶?"),
    Meme("whyatme", whyatme, ("为什么@我",), r"为什么(?:@|at)我"),
    Meme("decent_kiss", decent_kiss, ("像样的亲亲",)),
    Meme("jiujiu", jiujiu, ("啾啾",)),
    Meme("suck", suck, ("吸", "嗦")),
    Meme("hammer", hammer, ("锤",)),
    Meme("tightly", tightly, ("紧贴", "紧紧贴着")),
    Meme("distracted", distracted, ("注意力涣散",)),
    Meme("anyasuki", anyasuki, ("阿尼亚喜欢",)),
    Meme("thinkwhat", thinkwhat, ("想什么",)),
    Meme("keepaway", keepaway, ("远离",)),
    Meme("marriage", marriage, ("结婚申请", "结婚登记")),
    Meme("divorce", divorce, ("离婚协议", "离婚申请")),
    Meme("painter", painter, ("小画家",)),
    Meme("repeat", repeat, ("复读",)),
    Meme("anti_kidnap", anti_kidnap, ("防诱拐",)),
    Meme("charpic", charpic, ("字符画",)),
    Meme("mywife", mywife, ("我老婆",)),
    Meme("walnutpad", walnutpad, ("胡桃平板",)),
    Meme("walnut_zoom", walnut_zoom, ("胡桃放大",)),
    Meme("teach", teach, ("讲课", "敲黑板")),
    Meme("addition", addition, ("上瘾", "毒瘾发作")),
    Meme("gun", gun, ("手枪",)),
    Meme("blood_pressure", blood_pressure, ("高血压",)),
    Meme("read_book", read_book, ("看书",)),
    Meme("call_110", call_110, ("遇到困难请拨打",)),
    Meme("confuse", confuse, ("迷惑",)),
    Meme("hit_screen", hit_screen, ("打穿", "打穿屏幕"), r"打穿(?:屏幕)?"),
    Meme("fencing", fencing, ("击剑", "🤺")),
    Meme("hug_leg", hug_leg, ("抱大腿",)),
    Meme("tankuku_holdsign", tankuku_holdsign, ("唐可可举牌",)),
    Meme("no_response", no_response, ("无响应",)),
    Meme("hold_tight", hold_tight, ("抱紧",)),
    Meme("look_flat", look_flat, ("看扁",)),
    Meme("look_this_icon", look_this_icon, ("看图标",)),
    Meme("captain", captain, ("舰长",)),
    Meme("jiji_king", jiji_king, ("急急国王",)),
    Meme("incivilization", incivilization, ("不文明",)),
    Meme("together", together, ("一起",)),
    Meme("wave", wave, ("波纹",)),
    Meme("rise_dead", rise_dead, ("诈尸", "秽土转生")),
    Meme("kirby_hammer", kirby_hammer, ("卡比锤", "卡比重锤")),
    Meme("wooden_fish", wooden_fish, ("木鱼",)),
    Meme("karyl_point", karyl_point, ("凯露指",)),
    Meme("kick_ball", kick_ball, ("踢球",)),
    Meme("smash", smash, ("砸",)),
    Meme("bocchi_draft", bocchi_draft, ("波奇手稿",)),
    Meme("sit_still", sit_still, ("坐得住", "坐的住")),
    Meme("learn", learn, ("偷学",)),
    Meme("trance", trance, ("恍惚",)),
    Meme("dinosaur", dinosaur, ("恐龙", "小恐龙")),
    Meme("scratch_head", scratch_head, ("挠头",)),
    Meme("applaud", applaud, ("鼓掌",)),
    Meme("chase_train", chase_train, ("追列车", "追火车")),
    Meme("kaleidoscope", kaleidoscope, ("万花筒", "万花镜")),
    Meme("overtime", overtime, ("加班",)),
    Meme("avatar_formula", avatar_formula, ("头像公式", "等价无穷小")),
    Meme("potato", potato, ("土豆",)),
    Meme("printing", printing, ("打印",)),
    Meme("name_generator", name_generator, ("亚文化取名机", "亚名")),
]

memes = [meme for meme in memes if meme.name not in petpet_config.petpet_disabled_list]
