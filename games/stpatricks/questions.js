const DEFAULT_Q = {
  rounds: [
    { name: "Round One", values: [100,200,300,400,500], categories: [
      { name: "The Emerald Isle", qs: [
        { q: "What is the capital city of Ireland?", a: "Dublin", note: "Dublin sits on the River Liffey, on Ireland's east coast." },
        { q: "Which musical instrument is the national symbol of Ireland, shown on its coins and passports?", a: "The harp", note: "The model is a medieval harp kept at Trinity College Dublin, often called the Brian Boru harp." },
        { q: "What are the three colors of the Irish flag?", a: "Green, white and orange", note: "Green stands for the Gaelic tradition, orange for the supporters of William of Orange, and white for peace between them." },
        { q: "What is the longest river in Ireland?", a: "The River Shannon", note: "It runs for about 360 kilometers (224 miles), from County Cavan to the Atlantic." },
        { q: "Which famous sea cliffs on Ireland's west coast rise more than 200 meters (650 feet) above the Atlantic?", a: "The Cliffs of Moher", note: "They are in County Clare and reach about 214 meters (702 feet) at their highest point." }
      ]},
      { name: "Luck & Legends", qs: [
        { q: "How many leaves does a 'lucky' clover have?", a: "Four", note: "Most clovers have three leaves. Four-leaf clovers are rare, roughly one in several thousand." },
        { q: "According to legend, what does a leprechaun keep hidden at the end of the rainbow?", a: "A pot of gold", note: "Catch a leprechaun, the stories say, and he must tell you where his gold is hidden." },
        { q: "Kissing which stone, set high in a castle near Cork, is said to give you the 'gift of the gab'?", a: "The Blarney Stone", special: "cat", note: "Visitors lie on their backs and lean over a drop at the top of Blarney Castle to kiss it." },
        { q: "In old Irish folklore, what is a leprechaun's trade?", a: "Shoemaker", note: "In the tales, leprechauns mend the shoes of the fairies, which is why they are always busy." },
        { q: "In Irish folklore, what is a banshee said to do before a death in the family?", a: "Wail (keen)", note: "The name comes from the Irish 'bean sí', meaning 'woman of the fairy mound'." }
      ]},
      { name: "Myths of Ireland", qs: [
        { q: "Which coastline of about 40,000 stone columns in Northern Ireland was, in legend, built by a giant so he could cross to Scotland?", a: "The Giant's Causeway", note: "Geologists say the columns formed when lava from an ancient volcanic eruption cooled and cracked." },
        { q: "In Irish legend, Tír na nÓg is a magical land where no one ever does what?", a: "Grows old", note: "Its name means 'Land of the Young'." },
        { q: "In the legend 'The Children of Lir', a jealous stepmother turns four children into which birds?", a: "Swans", note: "The spell kept them as swans for 900 years." },
        { q: "Which legendary Irish hero gained all the world's wisdom by burning his thumb on the Salmon of Knowledge?", a: "Fionn mac Cumhaill (Finn McCool)", special: "cat", note: "Whenever he needed wisdom afterward, he only had to suck his thumb." },
        { q: "What was the name of the old Celtic festival that marked the start of summer on May 1?", a: "Bealtaine (Beltane)", note: "It was one of four seasonal festivals, with Samhain, Imbolc and Lughnasadh." }
      ]},
      { name: "Going Green", qs: [
        { q: "Which two colors of paint do you mix to make green?", a: "Blue and yellow", note: "On a screen, green is one of the three primary colors of light, with red and blue." },
        { q: "What green pigment lets plants turn sunlight into food?", a: "Chlorophyll", note: "It absorbs red and blue light and reflects green, which is why leaves look green." },
        { q: "Which famous American statue turned green over time because its copper skin weathered?", a: "The Statue of Liberty", note: "The green layer, called a patina, formed within a few decades and now protects the copper underneath." },
        { q: "Emeralds are a green variety of which mineral?", a: "Beryl", note: "Aquamarine is the same mineral in blue." },
        { q: "Which green fruit, once called the 'Chinese gooseberry', was renamed by New Zealand exporters in 1959?", a: "The kiwifruit", note: "It was named after the kiwi, New Zealand's small brown national bird." }
      ]},
      { name: "Around the World", qs: [
        { q: "Which US city dyes its river green every year for St. Patrick's Day?", a: "Chicago", note: "The tradition began in 1962. Oddly, the dye is an orange powder that turns the water green." },
        { q: "Which city holds the world's largest St. Patrick's Day parade, first marched in 1762?", a: "New York City", note: "The first parade took place 14 years before the US Declaration of Independence." },
        { q: "On St. Patrick's Day, which famous building with sail-shaped roofs is lit up green in Australia?", a: "The Sydney Opera House", note: "It is one of hundreds of landmarks around the world that 'go green' for the day." },
        { q: "Which Caribbean island, nicknamed 'the Emerald Isle of the Caribbean', has St. Patrick's Day as a public holiday?", a: "Montserrat", note: "Many of its early European settlers were Irish." },
        { q: "In what year did St. Patrick's Day become an official public holiday in Ireland?", a: "1903", special: "witch", note: "It became a bank holiday under the Bank Holiday (Ireland) Act of 1903." }
      ]}
    ]},
    { name: "Round Two", values: [200,400,600,800,1000], categories: [
      { name: "The Real St. Patrick", qs: [
        { q: "Saint Patrick is the patron saint of which country?", a: "Ireland", note: "He shares the title with Saint Brigid and Saint Columba." },
        { q: "According to tradition, St. Patrick used which three-leaf plant to explain the Holy Trinity?", a: "The shamrock", note: "The story first appears in writing many centuries after his death." },
        { q: "According to legend, St. Patrick drove which animals out of Ireland?", a: "Snakes", note: "Scientists say Ireland had no snakes at all after the last Ice Age, so the legend is only a story." },
        { q: "St. Patrick was not born in Ireland. Where was he born?", a: "In Roman Britain", note: "At 16 he was kidnapped by raiders and taken to Ireland as a slave. He escaped, then later returned as a missionary." },
        { q: "St. Patrick's Day is held on March 17. What does that date traditionally mark?", a: "The day he died", note: "He is thought to have died in the 5th century, but the exact year is unknown." }
      ]},
      { name: "Irish Words", qs: [
        { q: "In Ireland, what does the word 'craic' mean?", a: "Fun, a good time", note: "It is pronounced 'crack'. 'What's the craic?' means 'What's new?'" },
        { q: "The Irish toast 'Sláinte!' means what?", a: "Health (cheers)", note: "It is pronounced roughly 'SLAWN-cha'." },
        { q: "Which English word, meaning tiny broken pieces, comes from the Irish word 'smidiríní'?", a: "Smithereens", special: "cat", note: "'Smidirín' means a small fragment in Irish." },
        { q: "What is the Irish-language name for Ireland, used in its constitution?", a: "Éire", note: "The constitution says that in English the name of the state is Ireland." },
        { q: "'Taoiseach' is the title of which Irish official?", a: "The prime minister (head of government)", note: "It is pronounced 'TEE-shock' and means 'chief' or 'leader'." }
      ]},
      { name: "Famous Irish", qs: [
        { q: "Which Irish rock band, fronted by Bono, formed in Dublin in 1976?", a: "U2", note: "The band members met as students at Mount Temple Comprehensive School." },
        { q: "Which Irish writer wrote the 1726 satire 'Gulliver's Travels'?", a: "Jonathan Swift", note: "Swift was also dean of St. Patrick's Cathedral in Dublin." },
        { q: "Which Irish playwright, famous for his wit, wrote 'The Importance of Being Earnest'?", a: "Oscar Wilde", note: "The play opened in London in 1895." },
        { q: "Which Irish writer's novel 'Ulysses' takes place in Dublin on a single day, June 16, 1904?", a: "James Joyce", special: "cat", note: "Fans celebrate that date every year as Bloomsday, after the novel's hero, Leopold Bloom." },
        { q: "Which US president, elected in 1960, visited his ancestral home in County Wexford in 1963?", a: "John F. Kennedy", note: "He was the first Catholic president of the United States, and all eight of his great-grandparents were Irish." }
      ]},
      { name: "Music & Dance", qs: [
        { q: "Which Irish dance show began as a seven-minute interval act at the 1994 Eurovision Song Contest in Dublin?", a: "Riverdance", note: "It became a full stage show in 1995 and has been seen by millions around the world." },
        { q: "What is the name of the Irish frame drum, often played with a small stick called a tipper?", a: "The bodhrán", note: "It is pronounced 'BOW-rawn'." },
        { q: "Which Irish singer from County Donegal had a worldwide hit in 1988 with 'Orinoco Flow'?", a: "Enya", note: "She is one of Ireland's best-selling solo artists." },
        { q: "In traditional Irish step dancing, which part of the body do dancers keep very still?", a: "Their arms (upper body)", note: "All the speed and rhythm comes from the feet." },
        { q: "Which band from Limerick, fronted by Dolores O'Riordan, had a 1993 hit with 'Linger'?", a: "The Cranberries", note: "It became the band's first big international hit." }
      ]},
      { name: "A Taste of Ireland", qs: [
        { q: "Irish soda bread rises without any yeast. What makes it rise?", a: "Baking soda (with buttermilk)", note: "The acid in buttermilk reacts with the baking soda and makes bubbles." },
        { q: "Corned beef and cabbage is a St. Patrick's Day favorite in which country, more than in Ireland itself?", a: "The United States", note: "In Ireland, bacon and cabbage is the more traditional dish." },
        { q: "What is colcannon, a traditional Irish dish?", a: "Mashed potatoes with cabbage or kale", note: "It is a traditional dish for October 31, sometimes with a coin or a ring hidden inside." },
        { q: "Which vegetable's crop failure in the 1840s caused the Great Famine in Ireland?", a: "The potato", note: "About a million people died and more than a million emigrated, many to North America." },
        { q: "Boxty, a traditional dish from the north and west of Ireland, is a kind of what?", a: "Potato pancake", special: "witch", note: "It is made from grated raw potato mixed with mashed potato and flour." }
      ]}
    ]}
  ],
  final: { category: "Irish in America", q: "Which Irish-born naval officer from County Wexford is often called the 'Father of the American Navy'?", a: "John Barry", note: "He was the first commissioned officer of the US Navy after the American Revolution." },
  tiebreak: { q: "In what year did Ireland join the European Economic Community, today's European Union?", a: "1973", note: "Ireland, the United Kingdom and Denmark all joined on January 1, 1973." }
};
