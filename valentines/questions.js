const DEFAULT_Q = {
  rounds: [
    { name: "Round One", values: [100,200,300,400,500], categories: [
      { name: "Be My Valentine", qs: [
        { q: "Which winged little figure from Roman mythology shoots arrows that make people fall in love?", a: "Cupid", note: "His mother was Venus, the goddess of love. In Greek myth he is Eros." },
        { q: "At the end of a message, what do the letters 'XOXO' stand for?", a: "Hugs and kisses", note: "X is a kiss and O is a hug. People have signed letters with an X for a kiss since at least the 1700s." },
        { q: "Esther Howland, called the 'Mother of the American Valentine', began selling lace-trimmed cards in the 1840s in which US state?", a: "Massachusetts", note: "She ran her valentine business from Worcester and turned it into an assembly line staffed by women." },
        { q: "In which century did the English poet Geoffrey Chaucer write one of the earliest known links between St. Valentine's Day and romantic love?", a: "The 14th century", note: "In his poem 'Parlement of Foules', from around 1380, birds gather to choose their mates on Saint Valentine's Day." },
        { q: "Valentine's Day is often linked to which ancient Roman festival, held in mid-February?", a: "Lupercalia", note: "Lupercalia was a fertility festival held on February 15. Historians still debate whether it has any real connection to Valentine's Day." }
      ]},
      { name: "Sweet on You", qs: [
        { q: "What are the small candy hearts printed with messages like 'BE MINE' and 'HUG ME' called?", a: "Conversation hearts (Sweethearts)", note: "The New England Confectionery Company made Sweethearts for more than a century. Since 2018 the brand has belonged to the Spangler Candy Company." },
        { q: "Which country is the world's largest producer of cocoa beans?", a: "Côte d'Ivoire (Ivory Coast)", note: "It grows roughly 40 percent of the world's cocoa. Neighboring Ghana is second." },
        { q: "Richard Cadbury is credited with creating the first heart-shaped box of chocolates. In which decade?", a: "The 1860s", special: "cat", note: "He decorated the boxes himself, and people kept them long after the chocolates were gone to store letters and keepsakes." },
        { q: "Which ancient civilization drank chocolate as a bitter, spiced drink and used cacao beans as money?", a: "The Aztecs (the Maya before them)", note: "Sugar was added only after chocolate reached Europe in the 1500s." },
        { q: "White chocolate has no cocoa solids at all. Which part of the cacao bean does it contain?", a: "Cocoa butter", note: "In the United States, white chocolate must contain at least 20 percent cocoa butter." }
      ]},
      { name: "Famous Couples", qs: [
        { q: "In Shakespeare's play, Romeo is a Montague. Which family does Juliet belong to?", a: "The Capulets", note: "The play is set in Verona, where visitors still leave letters for Juliet." },
        { q: "Which queen of Egypt had famous romances with Julius Caesar and Mark Antony?", a: "Cleopatra", note: "She was Cleopatra VII, the last active ruler of the Ptolemaic Kingdom of Egypt." },
        { q: "Which Mughal emperor built the Taj Mahal in memory of his wife Mumtaz Mahal?", a: "Shah Jahan", note: "Work began around 1632 and took more than 20 years. He is buried there beside her." },
        { q: "In Greek myth, which musician traveled to the underworld to bring back his wife Eurydice?", a: "Orpheus", special: "cat", note: "He could lead her out as long as he did not look back. At the last moment, he looked back." },
        { q: "Which married couple shared the 1903 Nobel Prize in Physics with Henri Becquerel?", a: "Marie and Pierre Curie", note: "Marie Curie later won a second Nobel Prize, in Chemistry, in 1911." }
      ]},
      { name: "Say It with Flowers", qs: [
        { q: "What color of rose traditionally stands for romantic love?", a: "Red", note: "Red roses are by far the most popular flower for Valentine's Day." },
        { q: "Rather than romance, what does a yellow rose usually stand for today?", a: "Friendship", note: "In the Victorian language of flowers it could also mean jealousy. Today it means friendship and joy." },
        { q: "What is the name for the Victorian custom of sending secret messages through the choice of flowers?", a: "Floriography (the language of flowers)", note: "Dictionaries explained what each flower meant, so a bouquet could say what people could not say out loud." },
        { q: "Most cut flowers sold in the United States, including Valentine's roses, are flown in from which South American country?", a: "Colombia", note: "Colombia is the largest supplier of cut flowers to the US, followed by Ecuador." },
        { q: "Tulips are a symbol of the Netherlands, but in which empire were they first grown as garden flowers?", a: "The Ottoman Empire (today's Turkey)", note: "Tulips reached the Netherlands in the late 1500s. The 'tulip mania' price bubble peaked in 1637." }
      ]},
      { name: "Love at the Movies", qs: [
        { q: "In Disney's 'Beauty and the Beast' (1991), what enchanted flower is kept under a glass dome?", a: "A rose", note: "If the last petal falls before the Beast learns to love and be loved, the spell lasts forever." },
        { q: "In 'Titanic' (1997), what is the name of Leonardo DiCaprio's character?", a: "Jack Dawson", note: "Kate Winslet played Rose DeWitt Bukater." },
        { q: "Which 1989 romantic comedy with Billy Crystal and Meg Ryan asks whether men and women can ever be just friends?", a: "When Harry Met Sally...", note: "The script was written by Nora Ephron." },
        { q: "In 'Casablanca' (1942), what is the name of the nightclub owned by Humphrey Bogart's character?", a: "Rick's Café Américain", note: "Ingrid Bergman played Ilsa, the woman who walks back into Rick's life." },
        { q: "Which 1953 film, about a princess exploring Rome with an American reporter, won Audrey Hepburn the Oscar for Best Actress?", a: "Roman Holiday", special: "witch", note: "Gregory Peck played the reporter. It was Hepburn's first starring role in a Hollywood film." }
      ]}
    ]},
    { name: "Round Two", values: [200,400,600,800,1000], categories: [
      { name: "Love Songs", qs: [
        { q: "Which British band released 'All You Need Is Love' in 1967?", a: "The Beatles", note: "They first performed it on 'Our World', one of the first live TV shows broadcast around the globe." },
        { q: "Which singer had a 2003 hit with 'Crazy in Love', featuring Jay-Z?", a: "Beyoncé", note: "It was the lead single of her first solo album, 'Dangerously in Love'." },
        { q: "Which singer, known as the 'King of Rock and Roll', had a 1961 hit with 'Can't Help Falling in Love'?", a: "Elvis Presley", note: "He sang it in the film 'Blue Hawaii' and often closed his concerts with it." },
        { q: "Whitney Houston's 1992 hit 'I Will Always Love You' was written and first recorded by which country star?", a: "Dolly Parton", note: "Dolly Parton released it in 1974 as a goodbye to her mentor, Porter Wagoner." },
        { q: "Which Russian composer wrote the 1935 ballet 'Romeo and Juliet', famous for the 'Dance of the Knights'?", a: "Sergei Prokofiev", note: "The ballet had its first full performance in 1938, in Brno, in what is now the Czech Republic." }
      ]},
      { name: "Lovebirds", qs: [
        { q: "Which pink birds stand on one leg and gather in flocks called a 'flamboyance'?", a: "Flamingos", note: "Their pink color comes from pigments in the algae and shrimp they eat." },
        { q: "Lovebirds, the small parrots that sit close together in pairs, come from which continent?", a: "Africa", note: "They are native to mainland Africa and Madagascar." },
        { q: "In which sea creature does the male carry the eggs and give birth to the young?", a: "The seahorse", special: "cat", note: "The female places her eggs in a pouch on the male's belly, and he carries them until they hatch." },
        { q: "Which bird's males keep an egg warm on their feet through the Antarctic winter while the females are away at sea?", a: "The emperor penguin", note: "The males huddle together and go without food for about two months while the egg develops." },
        { q: "Prairie voles are famous in science for which behavior, rare among mammals?", a: "Forming lifelong pair bonds", note: "Studies of their brains helped show how oxytocin and vasopressin shape bonding." }
      ]},
      { name: "Love Around the World", qs: [
        { q: "In which city did so many 'love locks' cover the Pont des Arts bridge that its railings were replaced with glass panels in 2015?", a: "Paris", note: "The weight of the padlocks had become a danger to the bridge." },
        { q: "In Japan, women traditionally give chocolate on Valentine's Day. What is the day, one month later, when men return the favor?", a: "White Day (March 14)", note: "White Day began in Japan in the late 1970s and spread to South Korea, Taiwan and China." },
        { q: "In South Korea, people who got nothing on Valentine's Day or White Day gather on April 14 to eat noodles in black bean sauce. What is this day called?", a: "Black Day", note: "The noodle dish is called jajangmyeon." },
        { q: "In Wales, January 25 is a day of love named after which Welsh patron saint of lovers?", a: "Saint Dwynwen", special: "cat", note: "In Welsh it is Dydd Santes Dwynwen, and people send cards just as they do on Valentine's Day." },
        { q: "In Finland and Estonia, February 14 is not mainly about romance. What kind of day is it?", a: "Friendship Day", note: "In Finnish it is Ystävänpäivä, 'friend's day', and people send cards to friends." }
      ]},
      { name: "Science of the Heart", qs: [
        { q: "How many chambers does the human heart have?", a: "Four", note: "Two atria on top receive blood, and two ventricles below pump it out." },
        { q: "What is a normal resting heart rate for an adult, in beats per minute?", a: "60 to 100", note: "Well-trained athletes can have resting rates as low as 40." },
        { q: "Which hormone, nicknamed the 'love hormone' or 'cuddle hormone', is released during hugs and bonding?", a: "Oxytocin", note: "It is made in the hypothalamus and released by the pituitary gland." },
        { q: "Which extinct plant from ancient Libya, whose heart-shaped seed pod appeared on coins, is one theory for the origin of the heart symbol?", a: "Silphium", note: "The city of Cyrene grew rich trading it. It is one of several theories for where the heart shape came from." },
        { q: "'Broken heart syndrome', a real heart condition triggered by sudden stress or grief, is also known by which Japanese name?", a: "Takotsubo cardiomyopathy", note: "During an attack the heart's main chamber takes the shape of a takotsubo, a Japanese octopus trap." }
      ]},
      { name: "Words of Love", qs: [
        { q: "How do you say 'I love you' in French?", a: "Je t'aime", note: "In Spanish it is 'te quiero' or 'te amo', and in Italian 'ti amo'." },
        { q: "'Ich liebe dich' means 'I love you' in which language?", a: "German", note: "German speakers also say 'Ich hab dich lieb' to family and close friends." },
        { q: "Which English poet wrote the line 'How do I love thee? Let me count the ways'?", a: "Elizabeth Barrett Browning", note: "It is Sonnet 43 from 'Sonnets from the Portuguese', published in 1850. She married the poet Robert Browning." },
        { q: "Shakespeare's Sonnet 18 begins by asking whether the poet should compare his love to what?", a: "A summer's day", note: "The answer the poem gives is that the beloved is even 'more lovely and more temperate'." },
        { q: "The ancient Greeks had several words for love. Which one meant the love between friends?", a: "Philia", special: "witch", note: "Eros was romantic love, agape selfless love and storge the love within a family." }
      ]}
    ]}
  ],
  final: { category: "Royal Romance", q: "Which British king gave up the throne in 1936 so that he could marry the American Wallis Simpson?", a: "Edward VIII", note: "He reigned for less than a year. His brother became King George VI." },
  tiebreak: { q: "In what year did Hershey's Kisses first go on sale?", a: "1907", note: "For years they were wrapped by hand. A machine took over in 1921." }
};
