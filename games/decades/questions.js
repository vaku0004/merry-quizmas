const DEFAULT_Q = {
  rounds: [
    { name: "Round One", values: [100,200,300,400,500], categories: [
      { name: "Totally ’80s", qs: [
        { q: "Which round, yellow, dot-eating arcade character first appeared in 1980?", a: "Pac-Man", note: "Namco released it in Japan in 1980. It became one of the most famous video games of all time." },
        { q: "Which colorful cube puzzle, invented by a Hungarian architect, became a worldwide craze in the early 1980s?", a: "The Rubik's Cube", note: "Ernő Rubik invented it in 1974. It went on sale around the world in 1980." },
        { q: "Which singer's 1982 album 'Thriller' became the best-selling album of all time?", a: "Michael Jackson", note: "It has sold an estimated 70 million copies worldwide." },
        { q: "In 1981, which TV channel launched in the US by playing the music video 'Video Killed the Radio Star'?", a: "MTV", note: "MTV went on the air on August 1, 1981. The song is by the British band The Buggles." },
        { q: "Which wall, a symbol of the Cold War, opened in November 1989?", a: "The Berlin Wall", note: "The border opened on November 9, 1989. East and West Germany reunited less than a year later." }
      ]},
      { name: "All That ’90s", qs: [
        { q: "Which virtual pet from Japan, kept on a keychain, became a worldwide craze in 1997?", a: "Tamagotchi", note: "Bandai released it in Japan in 1996. Forget to feed it, and your pet would get sick." },
        { q: "In the TV show 'Friends', what is the name of the coffee shop where the friends hang out?", a: "Central Perk", note: "The show ran for ten seasons, from 1994 to 2004." },
        { q: "Which British girl group, with members nicknamed Scary, Sporty, Baby, Ginger and Posh, had a 1996 hit with 'Wannabe'?", a: "The Spice Girls", special: "cat", note: "'Wannabe' reached number one in more than 30 countries." },
        { q: "What was the name of the sheep that, in 1996, became the first mammal cloned from an adult cell?", a: "Dolly", note: "She was born at the Roslin Institute in Scotland." },
        { q: "Which Seattle band, fronted by Kurt Cobain, released the 1991 album 'Nevermind'?", a: "Nirvana", note: "Its single 'Smells Like Teen Spirit' helped bring grunge music to the world." }
      ]},
      { name: "Y2K & the 2000s", qs: [
        { q: "Which Apple music player, launched in 2001, promised '1,000 songs in your pocket'?", a: "The iPod", note: "The first model had a 5 GB hard drive and a scroll wheel." },
        { q: "Which social network did Mark Zuckerberg launch from his college dorm room in 2004?", a: "Facebook", note: "It started as 'TheFacebook', open only to Harvard students." },
        { q: "What was the 'Y2K bug' that people feared would crash computers on January 1, 2000?", a: "Many computers stored years with two digits, so 2000 could look like 1900", note: "Companies spent billions fixing it in advance, and very little went wrong." },
        { q: "Which video-sharing website was founded in 2005 and bought by Google in 2006?", a: "YouTube", special: "cat", note: "The first video ever uploaded, 'Me at the zoo', is 19 seconds long." },
        { q: "Which Nintendo console, released in 2006, was famous for its motion-sensing remote?", a: "The Wii", note: "Its bowling game turned many grandparents into gamers." }
      ]},
      { name: "Toys & Games", qs: [
        { q: "Which small plush toys filled with plastic pellets, made by Ty, sparked a collecting frenzy in the late 1990s?", a: "Beanie Babies", note: "Collectors kept the heart-shaped tags on, hoping the toys would be worth a fortune one day." },
        { q: "Which handheld Nintendo console, released in 1989, came with the game Tetris in North America?", a: "The Game Boy", note: "Tetris was created in 1984 by Alexey Pajitnov, a Soviet computer scientist." },
        { q: "Which Hasbro toy line of robots that change into vehicles launched in 1984?", a: "Transformers", note: "The toys came with a TV cartoon the same year." },
        { q: "Which talking, furry toy with big eyes was the must-have holiday gift of 1998?", a: "Furby", note: "Furbies seemed to 'learn' English over time, starting out speaking their own language." },
        { q: "Which game franchise, born in Japan in 1996, invites players to 'catch 'em all'?", a: "Pokémon", note: "The first games, Pokémon Red and Green, came out on the Game Boy." }
      ]},
      { name: "TV Time", qs: [
        { q: "Which animated family from the town of Springfield got its own TV show in 1989?", a: "The Simpsons", note: "It is the longest-running American scripted primetime series." },
        { q: "In the TV show 'Baywatch', what job do the main characters have?", a: "Lifeguards", note: "At its peak in the 1990s, it was one of the most-watched shows in the world." },
        { q: "Which 1990s children's TV show starred Tinky Winky, Dipsy, Laa-Laa and Po?", a: "Teletubbies", note: "The British show first aired in 1997." },
        { q: "Which reality show, first aired in the US in 2000, asks contestants on an island to 'outwit, outplay, outlast'?", a: "Survivor", note: "It was based on a Swedish show called 'Expedition Robinson'." },
        { q: "Which sitcom, famously called 'a show about nothing', ended in 1998 after nine seasons?", a: "Seinfeld", special: "witch", note: "It starred Jerry Seinfeld as a version of himself, a comedian in New York." }
      ]}
    ]},
    { name: "Round Two", values: [200,400,600,800,1000], categories: [
      { name: "Movie Flashback", qs: [
        { q: "In 'E.T. the Extra-Terrestrial' (1982), which candy does Elliott use to lure E.T.?", a: "Reese's Pieces", note: "Sales of the candy jumped after the film came out." },
        { q: "Which 1993 film brought dinosaurs back to life in an island theme park?", a: "Jurassic Park", note: "It was directed by Steven Spielberg, based on the novel by Michael Crichton." },
        { q: "Which 1997 film became the first to earn more than one billion dollars worldwide?", a: "Titanic", note: "It also won 11 Oscars, tying the record." },
        { q: "Which 1999 science-fiction film made 'bullet time', a slow-motion camera effect, famous?", a: "The Matrix", note: "Keanu Reeves played Neo." },
        { q: "Which film won the first ever Oscar for Best Animated Feature, for films of 2001?", a: "Shrek", note: "It beat 'Monsters, Inc.' and 'Jimmy Neutron: Boy Genius'." }
      ]},
      { name: "Chart Toppers", qs: [
        { q: "Which singer, called the 'Queen of Pop', had a 1985 hit with 'Material Girl'?", a: "Madonna", note: "She is often listed as the best-selling female recording artist of all time." },
        { q: "Which boy band had a 1999 hit with 'I Want It That Way'?", a: "The Backstreet Boys", note: "The group formed in Orlando, Florida, in 1993." },
        { q: "Which Canadian singer released the hugely successful 1995 album 'Jagged Little Pill'?", a: "Alanis Morissette", special: "cat", note: "It has sold more than 30 million copies." },
        { q: "Which 1984 charity single, organized by Bob Geldof and Midge Ure, raised money for famine relief in Ethiopia?", a: "Do They Know It's Christmas? (Band Aid)", note: "It led to the Live Aid concerts in London and Philadelphia in 1985." },
        { q: "Which British singer named her 2008 debut album '19', after her age when she wrote it?", a: "Adele", note: "Her later albums were named '21', '25' and '30'." }
      ]},
      { name: "Tech Flashback", qs: [
        { q: "What noisy device did people use in the 1990s to connect a home computer to the internet over a phone line?", a: "A dial-up modem", note: "While you were online, nobody could use the phone." },
        { q: "Which Microsoft operating system launched in 1995 with a brand-new 'Start' button?", a: "Windows 95", note: "Its launch ads used the Rolling Stones song 'Start Me Up'." },
        { q: "What does 'DVD' stand for?", a: "Digital Versatile Disc (first 'Digital Video Disc')", note: "DVDs went on sale in Japan in 1996 and in the US in 1997." },
        { q: "Which Canadian company made the BlackBerry smartphone?", a: "Research In Motion (RIM)", special: "cat", note: "The company was based in Waterloo, Ontario, and renamed itself BlackBerry in 2013." },
        { q: "In 1997, which IBM computer became the first to beat a reigning world chess champion, Garry Kasparov, in a match?", a: "Deep Blue", note: "It won the six-game match 3½ to 2½." }
      ]},
      { name: "Fads & Fashion", qs: [
        { q: "Which hairstyle, short at the front and long at the back, is described as 'business in the front, party in the back'?", a: "The mullet", note: "It was everywhere in the 1980s, from rock stars to hockey players." },
        { q: "What were the bracelets called that curled around your wrist with one slap, a school craze around 1990?", a: "Slap bracelets", note: "Some schools banned them because the metal strips inside could break through." },
        { q: "In a 1990s schoolyard craze, kids collected and played with flat, round cardboard discs. What were they called?", a: "Pogs", note: "The name came from a Hawaiian juice whose bottle caps were used in the first games." },
        { q: "Which dance move, made famous by Michael Jackson in 1983, makes a dancer look like they are walking forward while sliding backward?", a: "The moonwalk", note: "He first performed it on TV during the Motown 25 special." },
        { q: "Which brand of colorful foam clogs, first shown at a 2002 boat show, became a love-it-or-hate-it fashion trend?", a: "Crocs", note: "They were first made as boating shoes, because they float and don't slip." }
      ]},
      { name: "Headlines", qs: [
        { q: "Which country hosted the 2000 Summer Olympics in Sydney?", a: "Australia", note: "Cathy Freeman lit the Olympic flame and later won the 400 meters." },
        { q: "Which space telescope, launched in 1990, has taken some of the most famous pictures of the universe?", a: "The Hubble Space Telescope", note: "Its first pictures were blurry because of a flaw in its mirror. Astronauts fixed it in 1993." },
        { q: "Which tunnel, opened in 1994, links Britain and France under the sea?", a: "The Channel Tunnel", note: "It is about 50 kilometers (31 miles) long." },
        { q: "In 1997, the United Kingdom handed which territory back to China?", a: "Hong Kong", note: "The handover took place at midnight on June 30, 1997." },
        { q: "Which currency went into circulation as coins and notes in 12 European countries on January 1, 2002?", a: "The euro", special: "witch", note: "It had existed only for banks and electronic payments since 1999." }
      ]}
    ]}
  ],
  final: { category: "Inventions That Changed Everything", q: "In 1989, while working at CERN in Switzerland, Tim Berners-Lee proposed a system that changed everyday life. What was it?", a: "The World Wide Web", note: "The first website went online at CERN in 1991. It is still there today." },
  tiebreak: { q: "In what year was the first text message (SMS) sent?", a: "1992", note: "On December 3, 1992, engineer Neil Papworth sent 'Merry Christmas' to a colleague's phone." }
};
