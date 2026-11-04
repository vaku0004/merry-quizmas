const DEFAULT_Q = {
  rounds: [
    { name: "Round One", values: [100,200,300,400,500], categories: [
      { name: "Traditions Around the World", qs: [
        { q: "In Spain, how many grapes do people eat at midnight, one for each chime of the clock?", a: "Twelve", note: "One grape for each month of the coming year. Eating them all in time is harder than it sounds." },
        { q: "In which country do people go 'first-footing' after midnight, as part of Hogmanay?", a: "Scotland", note: "The first guest over the doorstep is said to bring luck, especially one carrying coal, salt or shortbread." },
        { q: "In Denmark, people jump off what piece of furniture at midnight to leap into the New Year?", a: "A chair", note: "Danes also leave broken plates on friends' doorsteps. A big pile means lots of friends." },
        { q: "On Brazil's beaches, people dressed in white jump over how many waves at midnight for luck?", a: "Seven", note: "One wish for each wave. Many also leave flowers in the sea for Iemanjá, the goddess of the sea." },
        { q: "In Japan, Buddhist temples ring their great bells how many times on New Year's Eve?", a: "108", note: "The ceremony is called joya no kane. Each ring stands for one of 108 earthly desires." }
      ]},
      { name: "Midnight Around the Globe", qs: [
        { q: "In New York's Times Square, what drops down a pole in the last 60 seconds of the year?", a: "A giant ball (the Times Square Ball)", note: "Today's ball is covered in thousands of crystal triangles and lit by LEDs." },
        { q: "Which famous London bell chimes in the New Year on British TV and radio?", a: "Big Ben", note: "Big Ben is the great bell. Its tower was named the Elizabeth Tower in 2012." },
        { q: "Which Australian city's Harbour Bridge and Opera House light up with one of the first big fireworks shows of the night?", a: "Sydney", note: "Sydney also holds a 'family' fireworks show at 9 p.m. for those who can't stay up." },
        { q: "Which Pacific island nation, home to Kiritimati, is the first country to welcome the New Year?", a: "Kiribati", note: "Its Line Islands are 14 hours ahead of Greenwich time (UTC+14)." },
        { q: "In which year did Samoa skip December 30 completely, moving to the other side of the International Date Line?", a: "2011", note: "Samoa went straight from December 29 to December 31, and from one of the last places to see the New Year to one of the first." }
      ]},
      { name: "Party Food & Drink", qs: [
        { q: "Which sparkling wine, named after a region of France, is the classic New Year's toast?", a: "Champagne", note: "Only sparkling wine from the Champagne region of France may carry the name." },
        { q: "In the American South, which beans are eaten on New Year's Day for luck, often in a dish called Hoppin' John?", a: "Black-eyed peas", note: "They often come with collard greens for money and cornbread for gold." },
        { q: "In Italy, lentils are eaten on New Year's Eve because they look like what?", a: "Coins", note: "They are often served with cotechino, a rich pork sausage." },
        { q: "What is the name of the Greek New Year's cake with a coin hidden inside?", a: "Vasilopita (St. Basil's cake)", note: "Whoever finds the coin in their slice is said to have luck all year." },
        { q: "Which round, fried Dutch treats, dusted with powdered sugar, are eaten in the Netherlands on New Year's Eve?", a: "Oliebollen", note: "The name means 'oil balls'. Many have raisins inside." }
      ]},
      { name: "New Year, New You", qs: [
        { q: "What do we call a promise to start or stop a habit in the New Year?", a: "A New Year's resolution", note: "The most popular ones are about exercise, eating better and saving money." },
        { q: "About 4,000 years ago, what did the ancient Babylonians often promise their gods at their New Year festival?", a: "To pay back their debts (and return borrowed things)", note: "Their new year began in spring, with a festival called Akitu." },
        { q: "Which month is named after Janus, the Roman god of beginnings, who has two faces looking forward and back?", a: "January", note: "Janus was also the god of doors and gateways." },
        { q: "In 'Dry January', what do people give up for the whole month?", a: "Alcohol", note: "It started as a campaign in the United Kingdom in 2013." },
        { q: "In 'Veganuary', what do people try for the whole month of January?", a: "Eating vegan (no meat, dairy or other animal products)", note: "The campaign began in the United Kingdom in 2014." }
      ]},
      { name: "Calendars & Time", qs: [
        { q: "How many days are there in a leap year?", a: "366", note: "The extra day is February 29." },
        { q: "The calendar used across most of the world today is named after which pope?", a: "Pope Gregory XIII (the Gregorian calendar)", note: "He introduced it in 1582." },
        { q: "Which Roman leader's calendar, which took effect in 45 BC, made January 1 the start of the year?", a: "Julius Caesar", note: "It is called the Julian calendar, and some churches still use it to set their holidays." },
        { q: "What is the extra second sometimes added to clocks to keep them in step with Earth's spin called?", a: "A leap second", note: "The last one was added on New Year's Eve 2016, so that night's clocks read 23:59:60." },
        { q: "Before 1752, in Britain and its American colonies, on which date did the new year officially begin?", a: "March 25", note: "A law of 1750 moved the start of the year to January 1, from 1752." }
      ]}
    ]},
    { name: "Round Two", values: [200,400,600,800,1000], categories: [
      { name: "Lunar New Year", qs: [
        { q: "How many animals are there in the Chinese zodiac?", a: "Twelve", note: "Each year belongs to one animal, so the cycle repeats every twelve years." },
        { q: "Which color is lucky at Lunar New Year, and is used for the envelopes of money given as gifts?", a: "Red", note: "The envelopes are called hongbao in Mandarin." },
        { q: "Which animal comes first in the Chinese zodiac?", a: "The Rat", note: "Legend says the rat won the great race by riding on the ox's back and jumping ahead at the finish." },
        { q: "What is the Vietnamese name for the Lunar New Year festival?", a: "Tết", note: "Its full name, Tết Nguyên Đán, means 'Festival of the First Morning'." },
        { q: "2026 was the Year of the Horse. Which animal follows the horse, for the Lunar New Year of 2027?", a: "The Goat (or Sheep)", note: "Lunar New Year 2027 begins in early February." }
      ]},
      { name: "Fireworks & Bubbles", qs: [
        { q: "What do we call the handheld firework on a stick that throws off bright sparks?", a: "A sparkler", note: "A sparkler can burn at over 1,000 °C (about 1,800 °F), much hotter than it looks." },
        { q: "Which country is believed to have invented fireworks, more than a thousand years ago?", a: "China", note: "The first ones were bamboo stalks that burst with a bang in the fire." },
        { q: "The bubbles in Champagne are made of which gas?", a: "Carbon dioxide", note: "It forms during a second fermentation, inside the bottle." },
        { q: "Blue is the hardest firework color to make. Which metal's compounds give fireworks a blue glow?", a: "Copper", note: "If the flame is too hot, the blue fades to white." },
        { q: "Fireworks get their red color from which element, named after a village in Scotland?", a: "Strontium", note: "It was found in rocks from the village of Strontian in the 1790s." }
      ]},
      { name: "Songs for Midnight", qs: [
        { q: "Which song, written down by the Scottish poet Robert Burns, is sung at midnight in many countries?", a: "Auld Lang Syne", note: "Burns sent it to a song collection in 1788, saying he had heard it from an old man." },
        { q: "In plain English, what does 'auld lang syne' mean?", a: "'Old long since', or times gone by", note: "The song asks whether old friends should be forgotten." },
        { q: "Which Swedish pop group sang 'Happy New Year', released in 1980?", a: "ABBA", note: "It was on their album 'Super Trouper'." },
        { q: "Which bandleader's orchestra played 'Auld Lang Syne' on American New Year's Eve broadcasts for almost fifty years?", a: "Guy Lombardo (and His Royal Canadians)", note: "Many Americans called him 'Mr. New Year's Eve'." },
        { q: "Which Irish rock band released the single 'New Year's Day' in 1983?", a: "U2", note: "It was on their album 'War'." }
      ]},
      { name: "New Year on Screen", qs: [
        { q: "In 'When Harry Met Sally...' (1989), at what kind of party does Harry tell Sally he loves her?", a: "A New Year's Eve party", note: "He runs across New York to reach her before midnight." },
        { q: "Which TV host created 'New Year's Rockin' Eve' in 1972 and was its face for four decades?", a: "Dick Clark", note: "He also hosted 'American Bandstand' for more than thirty years." },
        { q: "In which 1972 film does a giant wave turn an ocean liner upside down on New Year's Eve?", a: "The Poseidon Adventure", note: "The survivors must climb up through the ship to reach its bottom." },
        { q: "Which Billy Wilder film, starring Jack Lemmon and Shirley MacLaine, ends on New Year's Eve and won the Oscar for Best Picture?", a: "The Apartment (1960)", note: "It ends with a game of cards." },
        { q: "In 'Bridget Jones's Diary' (2001), at what kind of New Year's Day party does Bridget meet Mark Darcy?", a: "A turkey curry buffet", note: "That's where she resolves to start her diary." }
      ]},
      { name: "Countdown Numbers", qs: [
        { q: "What time does the clock show one minute before midnight?", a: "11:59 p.m.", note: "On a 24-hour clock it reads 23:59." },
        { q: "Which Roman numeral stands for 1,000?", a: "M", note: "So 2027 is written MMXXVII." },
        { q: "The 'Y2K bug' made people worry that computers would fail at midnight going into which year?", a: "2000", note: "Many old programs stored years with two digits, so 2000 looked like 1900." },
        { q: "Most years divisible by 4 are leap years. Which was NOT a leap year: 1900 or 2000?", a: "1900", note: "Century years are leap years only if they divide by 400, as 2000 does." },
        { q: "To two decimal places, how many days does it take Earth to go once around the Sun?", a: "About 365.24 days", note: "That extra quarter day is why we add a leap day about every four years." }
      ]}
    ]}
  ],
  final: { category: "Midnight History", q: "Times Square is named after which newspaper, whose new tower hosted the first New Year's Eve party there in 1904?", a: "The New York Times", note: "The paper's owner, Adolph Ochs, celebrated the tower's opening with fireworks." },
  tiebreak: { q: "In what year did the first New Year's Eve ball drop in Times Square?", a: "1907", note: "The first ball was made of iron and wood and lit by 100 light bulbs." }
};
