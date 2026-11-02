const DEFAULT_Q = {
  rounds: [
    { name: "Round One", values: [100,200,300,400,500], categories: [
      { name: "Deck the Halls", qs: [
        { q: "Under which plant are people traditionally supposed to kiss at Christmas?", a: "Mistletoe", note: "The kissing custom was popular in 18th-century England. Traditionally, a berry was picked off for every kiss." },
        { q: "What is the English name for the Christmas cake shaped like a log, known in French as bûche de Noël?", a: "Yule log", note: "It recalls the old custom of burning a huge log in the hearth over the Christmas season." },
        { q: "Prince Albert helped make the decorated Christmas tree popular in Britain. In which country did the tradition begin?", a: "Germany", note: "A famous 1848 drawing of Queen Victoria and Albert's family around their tree made it fashionable across the English-speaking world." },
        { q: "On what date does the first door of most Advent calendars open?", a: "December 1", note: "The church season of Advent starts on a Sunday, but most calendars simply count December 1 to 24." },
        { q: "Which 4th-century bishop of Myra, known for secret gift-giving, inspired the figure of Santa Claus?", a: "Saint Nicholas", note: "Myra was in what is now Turkey. The Dutch name Sinterklaas turned into Santa Claus in America." }
      ]},
      { name: "Oh, Canada!", qs: [
        { q: "Canada Post delivers children's letters to Santa at a special postal code. What is it?", a: "H0H 0H0", note: "Volunteer elves have helped Santa answer millions of letters since the program began in 1982." },
        { q: "Mummering, when people in costume and disguise visit neighbours at Christmas, is a tradition of which province?", a: "Newfoundland and Labrador", note: "Hosts have to guess who the mummers are before offering them a drink and a treat." },
        { q: "Which spiced meat pie is a classic dish at the French-Canadian Christmas Eve feast, the réveillon?", a: "Tourtière", note: "It is usually made with pork, and sometimes beef or game, seasoned with cloves and cinnamon.", special: "cat" },
        { q: "Every year Nova Scotia sends a giant Christmas tree to which American city, as thanks for its help after the 1917 Halifax Explosion?", a: "Boston", note: "Boston sent doctors, nurses and supplies within hours. The tree lights up Boston Common." },
        { q: "The Huron Carol, Canada's oldest Christmas song, was written around 1642 by Jesuit missionary Jean de Brébeuf. In which language?", a: "Wendat (Huron)", note: "The English words most people know today were written in 1926 by Jesse Edgar Middleton." }
      ]},
      { name: "Sweet Treats", qs: [
        { q: "What flavour is a classic red and white candy cane?", a: "Peppermint", note: "Candy canes were plain white at first. The red stripes were added around 1900." },
        { q: "Eggnog is made with milk, cream and sugar, plus which main ingredient that gives it its name?", a: "Eggs", note: "Many recipes also add nutmeg, and grown-up versions add rum, brandy or bourbon." },
        { q: "Gingerbread houses became popular in which country in the 1800s, after the Brothers Grimm published Hansel and Gretel?", a: "Germany", note: "In the fairy tale, the witch's house in the forest is made of bread and cake." },
        { q: "What is the name of the tall, domed Italian Christmas bread with candied fruit and raisins, first made in Milan?", a: "Panettone", note: "Its dough rises slowly over several days, which makes it light and fluffy.", special: "cat" },
        { q: "Stollen, a fruit bread covered in icing sugar, is the pride of the Christmas market in which German city?", a: "Dresden", note: "Dresden's market, the Striezelmarkt, dates back to 1434 and holds a Stollen festival with a giant loaf." }
      ]},
      { name: "Christmas at the Movies", qs: [
        { q: "In Home Alone (1990), which city is the McCallister family flying to when they leave Kevin behind?", a: "Paris", note: "Kevin is left alone in the family's house near Chicago." },
        { q: "What is the name of Will Ferrell's character, a human raised by elves, in the 2003 film Elf?", a: "Buddy", note: "Buddy travels from the North Pole to New York City to find his father." },
        { q: "In Dr. Seuss's How the Grinch Stole Christmas, what is the name of the Grinch's dog?", a: "Max", note: "The Grinch ties an antler to Max's head to make him look like a reindeer." },
        { q: "In It's a Wonderful Life (1946), what is the first name of George Bailey's guardian angel?", a: "Clarence", note: "Clarence Odbody is an angel second class who still has to earn his wings." },
        { q: "In Miracle on 34th Street (1947), Kris Kringle works as Santa at which New York department store?", a: "Macy's", note: "The film opens at the real Macy's Thanksgiving Day Parade." }
      ]},
      { name: "Snow & Ice", qs: [
        { q: "How many sides or points does a snowflake crystal have?", a: "Six", note: "Water molecules freeze into a hexagonal pattern, so every snowflake is built on six." },
        { q: "What do we call a large mass of snow that suddenly slides down a mountainside?", a: "An avalanche", note: "Western Canada's mountains see thousands of avalanches every winter." },
        { q: "What is the name of the snowman mascot of the Quebec Winter Carnival?", a: "Bonhomme", note: "Bonhomme Carnaval wears a red toque and a colourful sash called a ceinture fléchée." },
        { q: "At what temperature do the Celsius and Fahrenheit scales show the same number?", a: "Minus 40", note: "−40 °C is exactly −40 °F, a number many Prairie winters know well." },
        { q: "What is the name for the feathery white ice crystals that form on trees and grass on cold, clear nights?", a: "Hoarfrost", note: "It forms when water vapour turns straight into ice, skipping the liquid stage.", special: "witch" }
      ]}
    ]},
    { name: "Round Two", values: [200,400,600,800,1000], categories: [
      { name: "Santa's Workshop", qs: [
        { q: "In the 1823 poem 'A Visit from St. Nicholas', how many reindeer pull Santa's sleigh?", a: "Eight", note: "Rudolph came later, in 1939, so he is not in the poem." },
        { q: "Which of Santa's reindeer shares its name with the Roman god of love?", a: "Cupid", note: "The others in the poem are Dasher, Dancer, Prancer, Vixen, Comet, Donner and Blitzen." },
        { q: "In the Netherlands, Sinterklaas arrives in mid-November by steamboat. Which country is he said to sail from?", a: "Spain", note: "Dutch children leave out a shoe with a carrot for his horse." },
        { q: "Rudolph the Red-Nosed Reindeer was created in 1939 for a free booklet handed out by which department store chain?", a: "Montgomery Ward", note: "Copywriter Robert L. May wrote the story. Millions of copies were given away that first Christmas." },
        { q: "In the first version of 'A Visit from St. Nicholas', two reindeer were called Dunder and Blixem. What do these Dutch words mean?", a: "Thunder and lightning", note: "Later printings changed them to Donder and Blitzen. Today most people say Donner and Blitzen." }
      ]},
      { name: "Around the World", qs: [
        { q: "In which country is fried chicken from KFC a popular Christmas dinner?", a: "Japan", note: "It began with a 1974 ad campaign. Families often order their Christmas bucket weeks ahead." },
        { q: "In Mexico, what are the nine nights of candlelit processions before Christmas called?", a: "Las Posadas", note: "From December 16 to 24, people act out Mary and Joseph's search for shelter." },
        { q: "Which country gives London a giant Christmas tree for Trafalgar Square every year, as thanks for help in the Second World War?", a: "Norway", note: "The tradition started in 1947. The tree comes from the forests around Oslo.", special: "cat" },
        { q: "In Italy, which kind old witch flies on a broom to bring sweets to children on the night before January 6?", a: "La Befana", note: "Good children get sweets and naughty ones get a lump of coal, often made of black sugar." },
        { q: "In Catalonia, which smiling wooden log is 'fed' for weeks and then hit with sticks until it gives out sweets?", a: "Tió de Nadal", note: "It wears a red cap and a blanket. Children sing to it while they tap it on Christmas Eve or Day." }
      ]},
      { name: "Christmas Creatures", qs: [
        { q: "Krampus is a horned creature from Alpine folklore who travels with Saint Nicholas. Whom does he punish?", a: "Naughty children", note: "Saint Nicholas rewards good children, and Krampus deals with the rest." },
        { q: "In Iceland, how many mischievous Yule Lads visit children in the nights before Christmas?", a: "Thirteen", note: "They arrive one at a time, starting December 12, and leave gifts or rotten potatoes in shoes." },
        { q: "Which giant cat from Icelandic folklore is said to eat people who don't get new clothes before Christmas?", a: "The Yule Cat (Jólakötturinn)", note: "The legend encouraged people to finish their wool work before the holidays." },
        { q: "Krampusnacht, when people in Krampus costumes parade through Alpine towns, is held on which date?", a: "December 5", note: "It is the eve of Saint Nicholas Day, December 6.", special: "cat" },
        { q: "In a Ukrainian Christmas legend, which creature decorated a poor family's tree overnight, which is why it appears on tree ornaments?", a: "A spider", note: "In the story, the spider's webs turned to silver and gold in the morning light, the origin of tinsel." }
      ]},
      { name: "Holiday Hits", qs: [
        { q: "Who sang the 1994 hit 'All I Want for Christmas Is You'?", a: "Mariah Carey", note: "It first reached number one on the US Billboard Hot 100 in 2019, 25 years after its release." },
        { q: "Which Canadian singer from Burnaby, B.C., released the hugely popular 2011 album 'Christmas'?", a: "Michael Bublé", note: "Its songs return to the charts every December." },
        { q: "'Silent Night' was first performed on Christmas Eve 1818 in a small village church in which country?", a: "Austria", note: "Joseph Mohr wrote the words and Franz Xaver Gruber the music, in Oberndorf near Salzburg." },
        { q: "'White Christmas', one of the best-selling singles of all time, was written by which American songwriter?", a: "Irving Berlin", note: "Bing Crosby's 1942 recording has sold tens of millions of copies." },
        { q: "In December 1965, astronauts on which NASA mission played 'Jingle Bells' on a harmonica and bells, the first song played in space?", a: "Gemini 6A", note: "Wally Schirra and Tom Stafford first joked that they had spotted a UFO in a red suit." }
      ]},
      { name: "Christmas History", qs: [
        { q: "Which 1843 novella by Charles Dickens tells the story of Ebenezer Scrooge?", a: "A Christmas Carol", note: "The first printing sold out in days." },
        { q: "The first commercial Christmas cards were printed in 1843 in which country?", a: "England (United Kingdom)", note: "Sir Henry Cole ordered 1,000 cards because he had no time to write letters by hand." },
        { q: "What does the 'X' in 'Xmas' originally stand for?", a: "The Greek letter chi, for Christ", note: "Chi, written X, is the first letter of 'Christ' in Greek, so Xmas is centuries old, not a modern shortcut." },
        { q: "Electric Christmas tree lights were first shown in 1882 by Edward H. Johnson, a business partner of which inventor?", a: "Thomas Edison", note: "Johnson's tree in New York had 80 red, white and blue bulbs." },
        { q: "From 1659 to 1681, celebrating Christmas was against the law in the Massachusetts Bay Colony. Which group passed the ban?", a: "The Puritans", note: "Anyone caught celebrating could be fined five shillings.", special: "witch" }
      ]}
    ]}
  ],
  final: { category: "A Christmas Miracle", q: "In December 1914, during the First World War, British and German soldiers on the Western Front stopped fighting, sang carols and met in no man's land. What is this event called?", a: "The Christmas Truce", note: "The ceasefire was unofficial. In some places it lasted into the new year." },
  tiebreak: { q: "In what year did Gene Autry release his famous recording of 'Rudolph the Red-Nosed Reindeer'?", a: "1949", note: "It sold more than 2 million copies in its first year." }
};
