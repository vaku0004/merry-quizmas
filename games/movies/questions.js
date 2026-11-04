const DEFAULT_Q = {
  rounds: [
    { name: "Round One", values: [100,200,300,400,500], categories: [
      { name: "Animated Classics", qs: [
        { q: "In 'Finding Nemo' (2003), what kind of fish is Nemo?", a: "A clownfish", note: "Real clownfish live among the stinging tentacles of sea anemones, which protect them." },
        { q: "What is the name of the friendly snowman in Disney's 'Frozen' (2013)?", a: "Olaf", note: "He dreams of summer, not knowing what heat does to snow." },
        { q: "In 'Toy Story' (1995), what is the name of the space ranger toy?", a: "Buzz Lightyear", note: "'Toy Story' was the first feature film made entirely with computer animation." },
        { q: "Which Japanese animated film by Hayao Miyazaki won the Oscar for Best Animated Feature in 2003?", a: "Spirited Away", note: "Miyazaki won the award again in 2024, for 'The Boy and the Heron'." },
        { q: "What was Walt Disney's first full-length animated feature film, released in 1937?", a: "Snow White and the Seven Dwarfs", note: "Many in Hollywood called it 'Disney's Folly' before it became a huge hit." }
      ]},
      { name: "Superheroes", qs: [
        { q: "What is Spider-Man's real name?", a: "Peter Parker", note: "He first appeared in a comic book in 1962." },
        { q: "Which city does Batman protect?", a: "Gotham City", note: "Bruce Wayne lives at Wayne Manor, with the Batcave hidden underneath." },
        { q: "In 'Black Panther' (2018), what is the name of the hidden, high-tech African nation?", a: "Wakanda", note: "Its technology is powered by a rare metal called vibranium." },
        { q: "Which unbreakable metal is bonded to Wolverine's skeleton?", a: "Adamantium", note: "Hugh Jackman played Wolverine in films for 17 years." },
        { q: "Which 2008 film, starring Robert Downey Jr., launched the Marvel Cinematic Universe?", a: "Iron Man", note: "It ends with Tony Stark telling reporters, 'I am Iron Man.'" }
      ]},
      { name: "Movie Food", qs: [
        { q: "In 'Ratatouille' (2007), what kind of animal dreams of becoming a great chef in Paris?", a: "A rat", note: "His name is Remy, and he cooks by steering a young man's hair from under his hat." },
        { q: "Which snack became a movie-theater favorite in the United States during the Great Depression of the 1930s?", a: "Popcorn", note: "It was cheap, filling and easy to sell, and it helped many theaters survive." },
        { q: "In 'Willy Wonka & the Chocolate Factory' (1971), what does Charlie find in his chocolate bar?", a: "A golden ticket", note: "Only five golden tickets were hidden in chocolate bars around the world." },
        { q: "In 'Forrest Gump' (1994), what does Forrest's mother say life is like?", a: "A box of chocolates", note: "Because you never know what you're going to get." },
        { q: "In 'Breakfast at Tiffany's' (1961), what does Audrey Hepburn's character eat while looking into the jewelry store's window?", a: "A pastry (a Danish) and coffee", note: "The opening scene was filmed early in the morning on Fifth Avenue in New York." }
      ]},
      { name: "Famous Lines", qs: [
        { q: "Which film series is famous for the line 'May the Force be with you'?", a: "Star Wars", note: "The first film came out in 1977." },
        { q: "In 'The Wizard of Oz' (1939), who says 'There's no place like home'?", a: "Dorothy", note: "She has to click the heels of her ruby slippers three times." },
        { q: "Which actor said 'I'll be back' in 'The Terminator' (1984)?", a: "Arnold Schwarzenegger", note: "He went on to say versions of the line in many of his later films." },
        { q: "In 'Jaws' (1975), after seeing the shark, what does police chief Brody say they are going to need?", a: "A bigger boat", note: "The line was improvised by actor Roy Scheider." },
        { q: "Which 1972 crime film opens with the line 'I believe in America'?", a: "The Godfather", note: "It is said by the undertaker Bonasera, who has come to ask the Don for help." }
      ]},
      { name: "Sequels & Series", qs: [
        { q: "What is the name of the wizarding school in the 'Harry Potter' films?", a: "Hogwarts", note: "Students are sorted into four houses: Gryffindor, Hufflepuff, Ravenclaw and Slytherin." },
        { q: "Which secret agent is known by the code number 007?", a: "James Bond", note: "He was created by the British writer Ian Fleming in 1953." },
        { q: "In the 'Back to the Future' films, which car is turned into a time machine?", a: "A DeLorean", note: "It has to reach 88 miles per hour to travel through time." },
        { q: "Which archaeologist adventurer, played by Harrison Ford, is afraid of snakes?", a: "Indiana Jones", note: "His first adventure was 'Raiders of the Lost Ark' in 1981." },
        { q: "Which 2003 film won all 11 Oscars it was nominated for, including Best Picture?", a: "The Lord of the Rings: The Return of the King", note: "It tied the record for the most Oscars won by a single film." }
      ]}
    ]},
    { name: "Round Two", values: [200,400,600,800,1000], categories: [
      { name: "Behind the Scenes", qs: [
        { q: "What is the name of the hinged board snapped shut at the start of each shot?", a: "A clapperboard (slate)", note: "The snap helps editors match the sound to the picture." },
        { q: "In filmmaking, what does 'CGI' stand for?", a: "Computer-generated imagery", note: "'Jurassic Park' (1993) was a landmark for lifelike CGI creatures." },
        { q: "What color is the screen most often used behind actors, so backgrounds can be added later?", a: "Green", note: "Green is used because it is a color rarely found in skin tones and most costumes." },
        { q: "What job title is given to the person in charge of the camera and lighting, also called the cinematographer?", a: "Director of photography", note: "On set, the role is often shortened to 'DP'." },
        { q: "Which 1927 film was the first feature-length 'talkie' with synchronized dialogue?", a: "The Jazz Singer", note: "Before it, feature films were silent, with live music in the theater." }
      ]},
      { name: "Directors", qs: [
        { q: "Who directed 'Jaws', 'E.T.' and 'Jurassic Park'?", a: "Steven Spielberg", note: "He is one of the most commercially successful directors in history." },
        { q: "Which director, known as the 'Master of Suspense', made 'Psycho' and 'The Birds'?", a: "Alfred Hitchcock", note: "He made brief cameo appearances in many of his own films." },
        { q: "Which Canadian director made both 'Titanic' and 'Avatar'?", a: "James Cameron", note: "He was born in Kapuskasing, Ontario." },
        { q: "Which New Zealand director brought 'The Lord of the Rings' to the screen?", a: "Peter Jackson", note: "All three films were shot in New Zealand at the same time." },
        { q: "Who became the first woman to win the Oscar for Best Director, in 2010, for 'The Hurt Locker'?", a: "Kathryn Bigelow", note: "Only a handful of women have won the award since." }
      ]},
      { name: "Movie Music", qs: [
        { q: "Which composer wrote the music for 'Star Wars', 'Jaws' and 'Indiana Jones'?", a: "John Williams", note: "He has received more than 50 Oscar nominations, more than any other living person." },
        { q: "In 'The Sound of Music' (1965), in which country does the von Trapp family live?", a: "Austria", note: "The film is based on the real von Trapp family singers." },
        { q: "Which 1977 film, starring John Travolta, made disco music a worldwide craze?", a: "Saturday Night Fever", note: "Its soundtrack, featuring the Bee Gees, became one of the best-selling albums ever." },
        { q: "Which 1994 Disney film features songs by Elton John and Tim Rice, including 'Circle of Life'?", a: "The Lion King", note: "The story was later turned into one of the most successful Broadway musicals of all time." },
        { q: "Which Italian composer wrote the famous whistling theme for 'The Good, the Bad and the Ugly' (1966)?", a: "Ennio Morricone", note: "He wrote music for more than 400 films and TV shows." }
      ]},
      { name: "Hollywood History", qs: [
        { q: "What famous sign stands in the hills above Los Angeles?", a: "The Hollywood Sign", note: "It first read 'Hollywoodland', as an advertisement for a housing development, in 1923." },
        { q: "What is the name of the famous Los Angeles sidewalk with stars honoring entertainers?", a: "The Hollywood Walk of Fame", note: "It has more than 2,700 stars." },
        { q: "Which silent-film star was famous for his 'Little Tramp' character, with a bowler hat and a cane?", a: "Charlie Chaplin", note: "He was born in London in 1889." },
        { q: "Which 1939 film, set during the American Civil War, is often called the highest-earning film of all time when adjusted for inflation?", a: "Gone with the Wind", note: "Hattie McDaniel won an Oscar for it, the first ever won by a Black actor." },
        { q: "In what year were the first Academy Awards held?", a: "1929", note: "The ceremony lasted about 15 minutes, and the winners had been announced three months earlier." }
      ]},
      { name: "World Cinema", qs: [
        { q: "Which Indian city's film industry is nicknamed 'Bollywood'?", a: "Mumbai", note: "The name mixes 'Bombay', the city's former name, with 'Hollywood'." },
        { q: "Which South Korean film won the Oscar for Best Picture in 2020, the first non-English-language film to do so?", a: "Parasite", note: "It was directed by Bong Joon-ho." },
        { q: "The film industry nicknamed 'Nollywood', one of the largest in the world by number of films, is in which country?", a: "Nigeria", note: "It produces many hundreds of films every year, often on small budgets." },
        { q: "Which famous film festival is held every May on the French Riviera?", a: "The Cannes Film Festival", note: "Its top prize is the Palme d'Or, or Golden Palm." },
        { q: "Which French brothers held one of the first public film screenings for a paying audience, in Paris in 1895?", a: "The Lumière brothers", note: "Legend says that audiences ran from a film of a train pulling into a station." }
      ]}
    ]}
  ],
  final: { category: "Hollywood Legends", q: "Which actress holds the record for the most acting Oscars, with four wins for Best Actress?", a: "Katharine Hepburn", note: "She won in 1934, 1968, 1969 and 1982." },
  tiebreak: { q: "In what year was the first 'Star Wars' film released?", a: "1977", note: "It was released in May 1977 and later retitled 'Episode IV – A New Hope'." }
};
