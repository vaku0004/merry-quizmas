const DEFAULT_Q = {
  rounds: [
    { name: "Round One", values: [100,200,300,400,500], categories: [
      { name: "Planet Earth", qs: [
        { q: "What is the largest ocean on Earth?", a: "The Pacific Ocean", note: "It covers about a third of the planet's surface, more than all the land put together." },
        { q: "What is the longest river in Africa?", a: "The Nile", note: "It is often called the longest river in the world, though some measurements give that title to the Amazon." },
        { q: "What is the capital city of Australia?", a: "Canberra", note: "It was built as a compromise, because Sydney and Melbourne both wanted to be the capital." },
        { q: "What is the largest hot desert in the world?", a: "The Sahara", note: "The largest desert of all is Antarctica, because so little snow or rain falls there." },
        { q: "Mount Everest sits on the border between Nepal and which other country?", a: "China (Tibet)", note: "Its official height is 8,849 meters (29,032 feet)." }
      ]},
      { name: "Science Lab", qs: [
        { q: "Which gas do plants take in from the air to make their food?", a: "Carbon dioxide", note: "They give off oxygen in return." },
        { q: "What is the chemical symbol for gold?", a: "Au", note: "It comes from the Latin word for gold, 'aurum'." },
        { q: "What is the hardest natural substance on Earth?", a: "Diamond", special: "cat", note: "A diamond is made of pure carbon, the same element as the graphite in a pencil." },
        { q: "How many bones are in the adult human body?", a: "206", note: "Babies are born with around 300 bones, and many of them fuse together as they grow." },
        { q: "What is the only metal that is liquid at normal room temperature?", a: "Mercury", note: "Gallium comes close: it melts at about 30 °C (86 °F), so it melts in your hand." }
      ]},
      { name: "Food & Drink", qs: [
        { q: "Guacamole is made mainly from which fruit?", a: "Avocado", note: "Yes, botanically the avocado is a fruit: a large berry with a single seed." },
        { q: "What is the main ingredient of hummus?", a: "Chickpeas", note: "They are blended with tahini, lemon juice, garlic and olive oil." },
        { q: "Which spice, made from the threads of a crocus flower, is the most expensive in the world by weight?", a: "Saffron", note: "Each flower has only three threads, and they are picked by hand." },
        { q: "Which Italian city is the home of the pizza margherita?", a: "Naples", special: "cat", note: "Legend says it was named in 1889 for Queen Margherita, with toppings in the colors of the Italian flag." },
        { q: "Outside Japan, the 'wasabi' served with sushi is usually made mostly from which other plant?", a: "Horseradish", note: "Real wasabi is rare and expensive, so most of it is horseradish with mustard and green coloring." }
      ]},
      { name: "Animal Kingdom", qs: [
        { q: "What is the fastest land animal?", a: "The cheetah", note: "In short sprints it can reach about 100 km/h (over 60 mph)." },
        { q: "How many hearts does an octopus have?", a: "Three", note: "Two pump blood through the gills, and one pumps it around the body." },
        { q: "What is a baby kangaroo called?", a: "A joey", note: "A newborn joey is about the size of a jelly bean." },
        { q: "What is the largest animal known to have ever lived?", a: "The blue whale", note: "It can grow to about 30 meters (100 feet) long, bigger than any dinosaur." },
        { q: "Which is the only bird that can fly backward?", a: "The hummingbird", note: "Its wings can beat around 50 times a second, or even faster." }
      ]},
      { name: "Words & Wordplay", qs: [
        { q: "What is a word that reads the same forward and backward, like 'level', called?", a: "A palindrome", note: "Whole sentences can be palindromes too: 'Was it a car or a cat I saw?'" },
        { q: "Which letter appears most often in English writing?", a: "E", note: "The least common letters include Z, Q and X." },
        { q: "What do you call a word made from the first letters of other words, like NASA?", a: "An acronym", note: "NASA stands for National Aeronautics and Space Administration." },
        { q: "What is special about the sentence 'The quick brown fox jumps over the lazy dog'?", a: "It uses every letter of the alphabet (a pangram)", note: "Typists have used it for more than a century to test keyboards." },
        { q: "From which language does the English word 'kindergarten' come?", a: "German", special: "witch", note: "It means 'children's garden'. Friedrich Fröbel opened the first one in 1837." }
      ]}
    ]},
    { name: "Round Two", values: [200,400,600,800,1000], categories: [
      { name: "History Mystery", qs: [
        { q: "Which ancient civilization built Machu Picchu, high in the mountains of Peru?", a: "The Inca", note: "It was built in the 1400s and was rediscovered by the wider world in 1911." },
        { q: "Which ancient empire built the Colosseum in Rome?", a: "The Roman Empire", note: "It was completed in 80 AD and could hold around 50,000 spectators." },
        { q: "Which famous wall, about 21,000 kilometers long with all its branches, was built over many centuries in northern China?", a: "The Great Wall of China", note: "Contrary to popular belief, it cannot be seen from space with the naked eye." },
        { q: "Which British monarch reigned for 70 years, longer than any other?", a: "Queen Elizabeth II", note: "She reigned from 1952 until her death in 2022." },
        { q: "The Magna Carta, agreed in 1215, limited the power of which English king?", a: "King John", note: "It is one of the most famous documents in the history of democracy." }
      ]},
      { name: "Space", qs: [
        { q: "Which planet is known as the Red Planet?", a: "Mars", note: "Its red color comes from iron oxide, or rust, in its dust." },
        { q: "Who was the first person to walk on the Moon?", a: "Neil Armstrong", note: "He stepped onto the Moon on July 20, 1969, during the Apollo 11 mission." },
        { q: "What is the largest planet in our solar system?", a: "Jupiter", special: "cat", note: "More than 1,000 Earths could fit inside it." },
        { q: "About how long does sunlight take to reach Earth?", a: "About 8 minutes", note: "Light travels about 300,000 kilometers every second." },
        { q: "In 2006, which planet was reclassified as a dwarf planet?", a: "Pluto", note: "Astronomers decided a planet must clear its orbit of other objects, which Pluto does not." }
      ]},
      { name: "Numbers Game", qs: [
        { q: "How many sides does a hexagon have?", a: "Six", note: "Honeycomb cells are hexagons." },
        { q: "What is the Roman numeral for 50?", a: "L", note: "C is 100, D is 500 and M is 1,000." },
        { q: "How many minutes are in a full day?", a: "1,440", note: "24 hours times 60 minutes." },
        { q: "What is 15 percent of 200?", a: "30", special: "cat", note: "10 percent is 20 and 5 percent is 10, so 15 percent is 30." },
        { q: "What is the smallest prime number?", a: "2", note: "It is also the only even prime number." }
      ]},
      { name: "Sports & Games", qs: [
        { q: "How many players from one team are on a basketball court at a time?", a: "Five", note: "Basketball was invented in 1891 by James Naismith, a Canadian." },
        { q: "In which sport do players hit a shuttlecock over a net?", a: "Badminton", note: "A shuttlecock can leave the racket at more than 400 km/h." },
        { q: "How many squares are on a chessboard?", a: "64", note: "Eight rows of eight squares." },
        { q: "Which country has won the men's FIFA World Cup the most times?", a: "Brazil", note: "Brazil has won it five times." },
        { q: "In tennis, what word means a score of zero?", a: "Love", note: "Nobody knows for sure where the term comes from." }
      ]},
      { name: "Art & Music", qs: [
        { q: "Who painted the Mona Lisa?", a: "Leonardo da Vinci", note: "It hangs in the Louvre in Paris, behind bulletproof glass." },
        { q: "How many keys does a standard piano have?", a: "88", note: "52 white keys and 36 black keys." },
        { q: "Which Dutch artist painted 'The Starry Night' in 1889?", a: "Vincent van Gogh", note: "He painted it at an asylum in Saint-Rémy, in southern France, based on the view from his window." },
        { q: "Which composer kept writing music after losing his hearing, including his famous Ninth Symphony?", a: "Ludwig van Beethoven", note: "At its first performance in 1824 he had to be turned around to see the audience applauding." },
        { q: "Which Spanish artist co-founded Cubism and painted 'Guernica'?", a: "Pablo Picasso", special: "witch", note: "He founded Cubism with the French painter Georges Braque." }
      ]}
    ]}
  ],
  final: { category: "Wonders of the World", q: "Which is the only one of the Seven Wonders of the Ancient World that is still standing?", a: "The Great Pyramid of Giza", note: "It was the tallest structure made by humans for about 3,800 years." },
  tiebreak: { q: "How tall is the Eiffel Tower today, in meters, including its antennas?", a: "330", note: "It was about 300 meters tall when it opened in 1889. Antennas added over the years made it taller." }
};
