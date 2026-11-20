# Package spec: London & Europe Grand Tour, 17 April – 2 May 2027 (15 nights / 16 days, 8 countries by coach).
# General-audience edition (team request, Nov 2026): sells the sights, wonders and comfort to any Indian traveller;
# temple visits stay in the plan but are not the headline.
# Built with the punya-kshetras-brand skill. Field reference: .claude/skills/punya-kshetras-brand/engine/PACKAGE_SPEC.md
# Schedule: python3 make_rows.py (from ../itinerary_data.py) → rows.json ; photos: python3 make_imgmap.py
# Build:    bash ../../../.claude/skills/punya-kshetras-brand/engine/build.sh .
# Team decisions kept: price includes international flights; no driver tips or optional extras; no "Who can join" box;
# no photo credits printed; daily 07:30 programme, 08:00–09:00 breakfast, 09:00 departure.
PKG = {
 'key': 'ley27',
 'slug': 'London-Europe-Grand-Tour-16D-17-April-2-May-2027',
 'title': 'London & Europe',
 'title2': 'Grand Tour',
 'tagline': 'UK · France · Belgium · Netherlands · Germany · Switzerland · Italy · Vatican',
 'dates': '17 April – 2 May 2027',
 'dates_long': 'Saturday 17 April – Sunday 2 May 2027',
 'start_date': '2027-04-17',
 'duration': '15 Nights / 16 Days',
 'nights': 15,
 'days': 16,
 'price': '₹5,49,000',
 'gst_note': '+ 5% GST + 2% TCS',
 'price_note': 'per person · all-inclusive · including international flights & visas · the 2% TCS is credited back through your income-tax return',
 'seats_note': 'Limited seats – one coach only.',
 'kicker': '8 Countries · 65+ Attractions',
 'with_line': 'Escorted group tour from Hyderabad & Bangalore',
 'greeting': 'Namaste!',
 'closing': 'Bon voyage!',
 'hero': 'towerbridge',
 'hero_pos': '50% 45%',
 'cover_circles': [('colosseum', 'left:12mm;top:146mm'), ('eiffel', 'left:83mm;top:156mm'), ('titlis', 'left:154mm;top:146mm')],
 'cover_feats': ['Flights & visas included', '65+ attractions', '10 UNESCO World Heritage Sites',
                 'Indian vegetarian meals', 'Indian tour manager', 'Senior-friendly pace'],
 'stats': [(16, 'Days'), (8, 'Countries'), ('65+', 'Attractions'), (10, 'UNESCO sites'), ('3,500', 'Km by coach')],
 'welcome_title': ('Your dream holiday', 'to London & Europe'),
 'welcome_img': 'eiffel',
 'welcome_cap': 'The Eiffel Tower, Paris – you go up to the 2nd floor on Day 5',
 'quote': ('Travel is fatal to prejudice, bigotry, and narrow-mindedness.', 'The Innocents Abroad, 1869'),
 'quote_by': 'Mark Twain',
 'intro': "See the best of Europe in one unforgettable journey: 8 countries, 65+ attractions and 10 UNESCO World Heritage "
          "Sites in 16 days. Stand before the Colosseum, one of the New 7 Wonders of the World, and the Leaning Tower of "
          "Pisa; go up the Eiffel Tower; see the Koh-i-Noor at the Tower of London; touch the snow on Mount Titlis; ride a "
          "gondola in Venice and walk into the Sistine Chapel. Flights, visas, hotels, Indian vegetarian meals, entry "
          "tickets and a private coach are all included, so you simply pack and enjoy.",
 'org_line': "Organised by Punya Kshetras, the travel service of Hare Krishna Golden Temple, Hyderabad: a trusted, "
             "family-friendly group tour with an Indian tour manager, home-style Indian vegetarian food every day and "
             "special care for seniors.",
 'hl_title': 'Tour highlights',
 'highlights': ['Eiffel Tower, Louvre & Seine cruise',
                'Colosseum, Trevi Fountain & Pantheon',
                "Vatican, Sistine Chapel & St Peter's",
                'Leaning Tower of Pisa',
                'Venice gondola & St Mark’s Square',
                'Snow on Mount Titlis & Lucerne',
                'Eurostar under the English Channel',
                'Tower of London & the Koh-i-Noor',
                'London Eye · Madame Tussauds · British Museum',
                'Keukenhof tulips · Amsterdam canals',
                'Rhine Falls · Black Forest',
                'Milan Duomo · Atomium & Grand Place'],
 'stays': [('London', '3 Nights'), ('Paris', '2 Nights'), ('Benelux', '2 Nights'),
           ('Germany', '2 Nights'), ('Switzerland', '2 Nights'), ('Italy', '4 Nights')],
 'best': 'Late April is spring: tulips at their peak, long evenings, 15–21 °C by day and 6–11 °C at night. '
         'Mount Titlis is below zero, so carry a warm jacket and gloves.',
 'stops': [('Hyderabad / Bangalore', 'Flights on 17 April', 'Flight', 'via Dubai / Abu Dhabi'),
           ('London', '3 nights · Tower · London Eye · British Museum', 'Eurostar', 'Channel Tunnel'),
           ('Paris', '2 nights · Eiffel Tower · Louvre · Seine cruise', 'Coach', '305 km'),
           ('Brussels & the Ardennes', 'Atomium · Grand Place · fairy-tale château', 'Coach', '310 km'),
           ('Amsterdam', 'Canal cruise · windmills · Keukenhof tulips', 'Coach', '260 km'),
           ('Cologne', 'Cologne Cathedral · Hohenzollern Bridge', 'Coach', '480 km'),
           ('Black Forest & Zurich', 'Lake Titisee · Rhine Falls · Zurich', 'Coach', '85 km'),
           ('Titlis, Lucerne & Interlaken', 'Snow · Chapel Bridge · lake cruise', 'Coach', '265 km'),
           ('Bergamo & Milan', 'Hare Krishna village · Milan Duomo', 'Coach', '280 km'),
           ('Venice', 'Gondola · St Mark’s Square · Padova', 'Train', '4 h'),
           ('Rome & the Vatican', 'Sistine Chapel · Colosseum · Trevi Fountain', 'Coach', '360 km'),
           ('Pisa & Milan Malpensa', 'Leaning Tower · flights home on 2 May', '', '')],
 'journey_photos': [('colosseum', 'Colosseum, Rome'), ('eiffelnight', 'Eiffel Tower by night'), ('lucerne', 'Lucerne, Switzerland')],
 'attractions': {
   'header': 'Wonders & Attractions', 'sub': 'Everything below is included in the price',
   'wonders': [('colosseum', 'Colosseum, Rome', 'New 7 Wonders of the World'),
               ('pisa', 'Leaning Tower of Pisa', 'Wonder of the Medieval World'),
               ('eiffel', 'Eiffel Tower, Paris', '330 m icon of the world'),
               ('sistine', 'Sistine Chapel', "Michelangelo's masterpiece")],
   'countries': [
     ('United Kingdom', ['Buckingham Palace', 'Changing of the Guard', 'Tower of London',
                         'Crown Jewels & Koh-i-Noor', 'Tower Bridge', 'Trafalgar Square', 'London Eye',
                         'Big Ben & Houses of Parliament', 'Westminster Bridge', 'Madame Tussauds', 'British Museum', 'Eurostar through the Channel Tunnel']),
     ('France', ['Eiffel Tower (2nd floor)', 'Arc de Triomphe', 'Champs-Élysées', 'Place de la Concorde',
                 'Trocadéro', 'Notre-Dame', 'Île de la Cité', 'Louvre & Mona Lisa', 'Seine river cruise']),
     ('Belgium', ['Atomium', 'Grand Place', 'Manneken Pis', 'Galeries Royales Saint-Hubert', 'Château de Petite Somme', 'Museum of Sacred Art']),
     ('Netherlands', ['Amsterdam canal cruise', 'Zaanse Schans windmills', 'Clog & cheese workshops', 'Keukenhof tulip gardens']),
     ('Germany', ['Cologne Cathedral', 'Hohenzollern Bridge', 'Black Forest drive', 'Lake Titisee', 'Cuckoo-clock shops']),
     ('Switzerland', ['Rhine Falls', 'Zurich old town', 'Bahnhofstrasse', 'Lake Zurich', 'Grossmünster & Fraumünster', 'Mount Titlis snow & Rotair', 'Glacier Cave & Cliff Walk',
                      'Ice Flyer', 'Lion Monument', 'Chapel Bridge', 'Lucerne Old Town', 'Lake Lucerne cruise', 'Luzern–Interlaken Express']),
     ('Italy', ['Milan Duomo', 'Galleria Vittorio Emanuele II', 'La Scala', 'Basilica of St Anthony, Padova',
                'Prato della Valle', "St Mark's Square & Basilica", "Doge's Palace & Bridge of Sighs", 'Rialto Bridge', 'Venice gondola ride', 'Colosseum', 'Roman Forum', 'Trevi Fountain', 'Pantheon',
                'Leaning Tower, Cathedral & Baptistery of Pisa', 'Frecciarossa high-speed train']),
     ('Vatican City', ['Vatican Museums', 'Sistine Chapel', "St Peter's Basilica", "St Peter's Square"])],
   'unesco': ['Tower of London', 'Westminster', 'Paris, banks of the Seine', 'Grand Place, Brussels', 'Amsterdam canal ring',
              'Cologne Cathedral', 'Venice & its lagoon', 'Historic Rome', 'Vatican City', 'Piazza del Duomo, Pisa']},
 'daypages': [
  {'n': 1, 'title': 'Welcome to London', 'stay': 'London (Wembley)', 'imgs': ['bigben', 'westminster2'],
   'story': 'Fly from Bangalore (Etihad via Abu Dhabi, landing Heathrow 12:45 pm) or Hyderabad (Emirates via Dubai, landing '
            '6:40 pm). Our tour manager meets you at Heathrow and takes you by private coach to Wembley. Welcome '
            'get-together, a short briefing and a hot Indian dinner.',
   'sig': ('Did you know?', '"Big Ben" is really the name of the giant 13.7-tonne bell inside the clock tower. The tower '
           'itself is called the Elizabeth Tower.')},
  {'n': 2, 'title': 'Madame Tussauds · British Museum · Bhaktivedanta Manor', 'stay': 'London (Wembley)', 'imgs': ['londoneye', 'manor'],
  'story': "Pose with Bollywood stars, royals and world leaders at Madame Tussauds, then have lunch at the temple in Soho and "
           "walk to the British Museum for the Rosetta Stone, Egyptian mummies and its Indian galleries. In the evening, visit "
           "Bhaktivedanta Manor, the country house that Beatle George Harrison gave to the Hare Krishna movement, after a "
           "short stop at the Akshaya Patra kitchen in Watford.",
  'sig': ('Did you know?', 'The British Museum holds about 8 million objects and is free to enter. Its South Asia gallery has '
          'carvings from the Amaravati stupa in Andhra Pradesh.')},
 {'n': 3, 'title': 'Royal London: Palace, Crown Jewels & London Eye', 'stay': 'London (Wembley)', 'imgs': ['buckingham', 'crownjewels'],
  'story': "Watch the Changing of the Guard at Buckingham Palace. At the Tower of London, see the Crown Jewels and the famous "
           "Koh-i-Noor, then walk onto Tower Bridge. Photos at Trafalgar Square, a ride on the London Eye, dinner, and Big Ben "
           "and the Houses of Parliament lit up at night.",
  'sig': ('A Hyderabad connection', 'The Koh-i-Noor was mined in the old Golconda kingdom, near our own Hyderabad. Today it '
          'sits in a crown in the Jewel House at the Tower of London.')},
 {'n': 4, 'title': 'Eurostar to Paris · Notre-Dame & Seine cruise', 'stay': 'Paris', 'imgs': ['arcchamps', 'notredame'],
  'story': 'An early start with a packed breakfast for the 8 am Eurostar, which races under the English Channel and reaches '
           'Paris by late morning. After an Indian lunch, a Paris orientation: the Arc de Triomphe, the Champs-Élysées, '
           'Notre-Dame and the Île de la Cité, then a cruise on the Seine and an evening at the Paris Hare Krishna temple.',
  'sig': ('Did you know?', 'The Channel Tunnel runs about 50 km, nearly 38 km of it under the sea. Civil engineers named it '
          'one of the Seven Wonders of the Modern World.')},
 {'n': 5, 'title': 'The Louvre & the Eiffel Tower', 'stay': 'Paris', 'imgs': ['louvre', 'eiffel'],
  'story': 'A guided morning at the Louvre, the world’s most-visited museum, to see the Mona Lisa, the Venus de Milo and the '
           'Winged Victory. In the afternoon, take the lift up the Eiffel Tower to the 2nd floor, then the classic group '
           'photo from the Trocadéro.',
  'sig': ('Did you know?', 'The 330 m Eiffel Tower was the tallest structure in the world for 41 years. At night it sparkles '
          'with 20,000 lights for five minutes every hour.')},
 {'n': 6, 'title': 'Paris → Brussels: Atomium & Grand Place', 'stay': 'Brussels', 'imgs': ['atomium', 'grandplace'],
  'story': 'Drive to Brussels for lunch, a photo at the giant Atomium, then a walking tour of the golden Grand Place, the '
           'cheeky Manneken Pis and the elegant Galeries Royales Saint-Hubert, with time for Belgian waffles and chocolate.',
  'sig': ('Did you know?', 'The Atomium is a 102 m model of an iron crystal, magnified 165 billion times, built for the 1958 '
          'World Expo.')},
 {'n': 7, 'title': 'Fairy-tale Château → Amsterdam Canals', 'stay': 'Amsterdam', 'imgs': ['radhadesh', 'amsterdam'],
   'story': 'Drive into the green Ardennes hills to the Château de Petite Somme, a fairy-tale castle that is home to the '
            'Radhadesh temple, for lunch and a walk in its gardens. Continue to Amsterdam for an evening canal cruise past '
            'tall gabled houses.',
   'sig': ('Did you know?', 'Amsterdam has 165 canals and about 1,500 bridges, and its 17th-century canal ring is a UNESCO '
           'World Heritage Site.')},
  {'n': 8, 'title': 'Windmills & Keukenhof Tulips → Cologne Cathedral', 'stay': 'Cologne', 'imgs': ['keukenhof', 'zaanse'],
  'story': 'See working windmills, clog-making and a cheese farm at Zaanse Schans, then spend the afternoon among millions of '
           'tulips at Keukenhof, the world’s most famous flower garden. Drive on to Cologne for its soaring Gothic cathedral.',
  'sig': ('Did you know?', 'Keukenhof plants about 7 million bulbs every year and is open for only eight weeks in spring. '
          'Late April is the best time to see it.')},
 {'n': 9, 'title': 'Cologne → Goloka Dham → the Black Forest', 'stay': 'Titisee (Black Forest)', 'imgs': ['cologne', 'cologne2'],
  'story': 'Visit the Hare Krishna temple in Cologne and a peaceful farm community in the countryside for its Sunday '
           'programme, then drive south through the Black Forest to Lake Titisee for the night.',
  'sig': ('Did you know?', 'Cologne Cathedral took 632 years to finish (1248–1880). Its twin spires are 157 m tall.')},
 {'n': 10, 'title': 'Lake Titisee · Rhine Falls → Zurich', 'stay': 'Zurich', 'imgs': ['rhinefalls', 'zurich'],
   'story': "Walk by Lake Titisee and watch a cuckoo-clock demonstration, then feel the spray of the mighty Rhine Falls. "
            "In Zurich, stroll the Bahnhofstrasse and the lake promenade, and visit the city's Hare Krishna temple.",
   'sig': ('Did you know?', 'The Rhine Falls is the most powerful waterfall in Europe. In spring, when the Alpine snow melts, '
           'it is at its mightiest.')},
  {'n': 11, 'title': 'Snow on Mount Titlis · Lucerne → Interlaken', 'stay': 'Interlaken', 'imgs': ['titlis', 'lucerne'],
  'story': "Ride the revolving Rotair cable car up Mount Titlis to play in the snow, walk through the Glacier Cave, cross "
           "the Cliff Walk and ride the Ice Flyer. In Lucerne, see the Lion Monument and Chapel Bridge, cruise the lake for an "
           "hour and take the scenic Luzern–Interlaken Express.",
  'sig': ('Did you know?', 'The Rotair was the world’s first revolving cable car, and the Titlis Cliff Walk is Europe’s '
          'highest suspension bridge, at over 3,000 m.')},
 {'n': 12, 'title': 'Swiss Alps → Bergamo → Milan by evening', 'stay': 'Milan', 'imgs': ['interlaken', 'milan'],
  'story': 'Drive through the Swiss Alps by the Gotthard into Italy, with lunch at a Hare Krishna village community near '
           'Bergamo. In the evening, see the marble Milan Duomo, the glass-roofed Galleria Vittorio Emanuele II and La Scala.',
  'sig': ('Did you know?', 'Milan Cathedral took nearly six centuries to complete and has about 3,400 statues, more than any '
          'other building in the world.')},
 {'n': 13, 'title': 'Prabhupada Desh · Padova → Venice Gondola', 'stay': 'Venice-Mestre', 'imgs': ['venice', 'venice2'],
  'story': 'Visit the temple in the Berici hills, then the Basilica of St Anthony and the vast Prato della Valle in Padova. Sail '
           "into Venice for St Mark's Square, the Doge's Palace, the Bridge of Sighs, the Rialto Bridge and a gondola ride.",
  'sig': ('Did you know?', 'Venice is built on 118 small islands linked by more than 400 bridges, and there are no cars at '
          'all: everyone travels by boat or on foot.')},
 {'n': 14, 'title': 'High-speed Train to Rome & the Vatican', 'stay': 'Rome', 'imgs': ['sistine', 'stpeters'],
  'story': "An early high-speed train to Rome. With licensed guides, see the Vatican Museums and the Sistine Chapel, then St "
           "Peter's Basilica and St Peter's Square. Evening at leisure and dinner in Rome.",
  'sig': ('Did you know?', 'The Vatican is the smallest country on earth – our 8th country. Michelangelo painted the Sistine '
          'Chapel ceiling, about 500 square metres, between 1508 and 1512.')},
 {'n': 15, 'title': 'Colosseum & Trevi → the Leaning Tower of Pisa', 'stay': 'Pisa', 'imgs': ['colosseum', 'pisa'],
  'story': "See the Colosseum and the Roman Forum, toss a coin into the Trevi Fountain and step into the Pantheon. Lunch at a "
           "Tuscan villa temple among vineyards near Florence, then on to Pisa for the famous photo with the Leaning Tower "
           "and a farewell dinner.",
  'sig': ('Did you know?', 'The Colosseum held about 50,000 spectators and was voted one of the New 7 Wonders of the World in '
          '2007. The Leaning Tower of Pisa leans about 4 degrees.')},
 {'n': 16, 'title': 'Flights Home with a Lifetime of Memories', 'stay': None, 'imgs': ['eiffelnight', 'colosseumair'],
   'story': 'An early drive from Pisa to Milan Malpensa, then flights home: Hyderabad group on Emirates via Dubai (landing 3:05 am), '
            'Bangalore group on Etihad via Abu Dhabi (landing 3:15 am) on Monday 3 May.',
   'sig': ('Your tour in numbers', '16 days · 8 countries · 65+ attractions · 10 UNESCO World Heritage Sites · about 3,500 km '
           'by private coach, plus the Eurostar, boats and high-speed trains.')}],
 'places_header': ('Picture-Perfect Moments', 'The sights you will remember for life'),
 'places_title': ('Postcard moments', 'waiting for you'),
 'places': [('colosseum', 'Colosseum, Rome', 'New 7 Wonders of the World'),
            ('eiffel', 'Eiffel Tower, Paris', 'Up to the 2nd floor'),
            ('pisa', 'Leaning Tower of Pisa', 'The famous photo stop'),
            ('stpeters2', "St Peter's, Vatican", 'Vatican Museums & Sistine Chapel'),
            ('venice', 'Venice', "Gondola ride and St Mark's Square"),
            ('titlis', 'Mount Titlis', 'Snow at 3,020 m'),
            ('keukenhof', 'Keukenhof', 'Millions of spring tulips'),
            ('towerbridge', 'Tower Bridge, London', 'Tower Bridge and the Tower of London'),
            ('trevi', 'Trevi Fountain, Rome', 'Toss a coin to return to Rome')],
 'incl': ['International flights from Hyderabad or Bangalore (economy, group fares)',
          'UK and Schengen visa charges',
          '15 nights in hotels, twin sharing',
          'All meals – Indian vegetarian, breakfast, lunch and dinner',
          'Private coaches, Eurostar London–Paris, all boats and the Swiss and Italian trains in the plan',
          'Entry tickets to every attraction in the itinerary',
          'Indian tour manager throughout and licensed local guides'],
 'excl': ['GST 5% and TCS 2%', 'Personal expenses and shopping', 'Anything not listed under inclusions'],
 'flights': ['Hyderabad group: Emirates EK 527 / EK 3 via Dubai, Sat 17 April, dep 10:15 am, landing Heathrow 6:40 pm',
             'Bangalore group: Etihad EY 233 / EY 63 via Abu Dhabi, Sat 17 April, dep 4:35 am, landing Heathrow 12:45 pm',
             'Return Sun 2 May: Emirates EK 102 / EK 524 Milan → Dubai → Hyderabad (3:05 am, 3 May); Etihad EY 82 / EY 232 Milan → Abu Dhabi → Bangalore (3:15 am, 3 May)'],
 'flights_title': 'Flights · booked by us',
 'meal_note': 'All breakfasts, lunches and dinners are included: home-style Indian vegetarian food at hotels and selected '
              'Indian restaurants, so you never have to hunt for a meal abroad. No onion or garlic on request.',
 'why_title': ('Why travel', 'with us'),
 'experiences': ['Music & fun on the coach', 'Expert guides & stories', 'Comfortable hotels', 'Relaxed pace',
                 'Special care for seniors', 'Indian vegetarian food'],
 'why': [('Everything included', 'Flights, visas, hotels, meals, entry tickets and transfers in one clear price'),
         ('Indian food every day', 'Home-style vegetarian breakfast, lunch and dinner – no hunting for food abroad'),
         ('Indian tour manager', 'One person who speaks your language looks after you from Hyderabad to home'),
         ('Care for seniors', 'Seats near the front, lifts and wheelchairs where needed, an unhurried pace'),
         ('Visa help', 'We guide you through the UK and Schengen visa paperwork, step by step'),
         ('Family-like group', 'Travel with like-minded Indian families; make friends for life'),
         ('Trusted organiser', 'Run by Hare Krishna Golden Temple, Hyderabad, with years of group-tour experience')],
 'extra_terms': [('Visas', 'UK and Schengen visas are applied for by each traveller with our help; the visa fees are '
                  'included. Please give us your documents on time. If a visa is refused, the cancellation terms apply to '
                  'the costs already paid to airlines and hotels.'),
                 ('Flights & connections', 'Flights are booked on group fares and cannot be changed. If an airline or train '
                  'changes its schedule or a strike affects travel, our team will arrange the best alternative.')],
 'faq_common': [('What do I need for the visa?', 'A passport valid 3+ months after 3 May 2027 with 2 blank pages, Schengen-size '
                 'photos, income-tax returns, bank statements and a covering letter. We guide you through every step.'),
                ('What food is served?', 'Indian vegetarian food for every meal, at hotels and Indian restaurants. No onion '
                 'or garlic on request.')],
 'faq': [('How much walking is there?', 'City days have 10,000–15,000 steps at an easy pace. The coach drops us close to each '
          'place, and lifts are used wherever available.'),
         ('Will there be time for shopping?', 'Yes – the Champs-Élysées, Brussels, Lucerne, Milan and Venice all have '
          'free time for shopping and photos.')],
 'pack': ['Passport, visa copies, photo ID',
          'Warm jacket, gloves, woollen cap',
          'Walking shoes already broken in',
          'Raincoat or umbrella',
          'Personal medicines with prescriptions',
          'Universal plug adapter, power bank',
          'Sunglasses and a cap'],
 'dos': ['Carry your passport on travel days',
         'Be at the coach 5 minutes early',
         'Dress modestly for churches and the Vatican',
         'Use the buddy system; keep your phone charged',
         'Keep coins for toilets (€0.50–€1)',
         'Drink plenty of water'],
 'donts': ["Don't carry valuables in back pockets",
           "Don't accept 'free' bracelets or roses",
           "Don't leave the group without telling the tour manager",
           "Don't take meat, dairy or fresh produce into the UK/EU",
           "Don't buy from street sellers near monuments",
           "Don't take photos where signs prohibit it"],
 'back': 'venice2',
 'rows': 'rows.json',
 'timing_note': 'Timings are indicative and may change with flight slots, weather and queues. Distances by road are approximate.',
 'poster': {'hero': 'towerbridge', 'pos': '50% 45%', 'circ': ['colosseum', 'eiffel', 'titlis'],
            'kicker': '8 Countries · 65+ Attractions',
            'price_small': '+ 5% GST + 2% TCS · per person · incl. flights & visas',
            'hl': ['Eiffel Tower, Louvre & Seine cruise',
                   'Colosseum – a New 7 Wonder of the World',
                   'Leaning Tower of Pisa',
                   "Vatican, Sistine Chapel & St Peter's",
                   'Snow on Mount Titlis · Lucerne',
                   'Venice gondola · Milan Duomo',
                   'Tower of London & the Koh-i-Noor',
                   'Flights, visas & Indian meals included']},
}
