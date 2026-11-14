# Package spec: London & Europe Yatra, 17 April – 2 May 2027 (15 nights / 16 days, 8 countries by coach).
# Built with the punya-kshetras-brand skill. Field reference: .claude/skills/punya-kshetras-brand/engine/PACKAGE_SPEC.md
# Schedule: python3 make_rows.py (from ../itinerary_data.py) → rows.json
# Build:    bash ../../../.claude/skills/punya-kshetras-brand/engine/build.sh .
# Team decisions kept here: price includes international flights; no driver tips or optional extras;
# no "Who can join" box; no photo credits printed; daily 07:30 programme, 08:00–09:00 breakfast, 09:00 departure.
PKG = {
 'key': 'ley27',
 'slug': 'London-Europe-Yatra-16D-17-April-2-May-2027',
 'title': 'London & Europe',
 'title2': 'Yatra',
 'tagline': 'UK · France · Belgium · Netherlands · Germany · Switzerland · Italy · Vatican',
 'dates': '17 April – 2 May 2027',
 'dates_long': 'Saturday 17 April – Sunday 2 May 2027',
 'start_date': '2027-04-17',
 'duration': '15 Nights / 16 Days',
 'nights': 15,
 'days': 16,
 'price': '₹5,49,000',
 'gst_note': '+ 5% GST + 2% TCS',
 'price_note': 'per person · all-inclusive · including international flights · the 2% TCS is credited back through your income-tax return',
 'seats_note': 'Limited seats.',
 'kicker': '8 Countries · 10 ISKCON Temples',
 'hero': 'towerbridge',
 'hero_pos': '50% 40%',
 'cover_circles': [('manor', 'left:12mm;top:146mm'), ('eiffel', 'left:83mm;top:156mm'), ('titlis', 'left:154mm;top:146mm')],
 'cover_feats': ['International flights included', '8 countries by coach', '10 ISKCON temples',
                 'Snow on Mount Titlis', 'Vatican & Colosseum', 'Kirtan & sthala purana'],
 'stats': [(16, 'Days'), (15, 'Nights'), (8, 'Countries'), (10, 'ISKCON temples'), ('4,000', 'Km by coach')],
 'intro': "Travel with Hare Krishna devotees through eight countries in sixteen days. Take darshan at ten ISKCON temples, "
          "beginning with Srila Prabhupada's Bhaktivedanta Manor and the castle temple of Radhadesh, and see Europe's great "
          "sights, from the Tower of London and the Eiffel Tower to the snows of Mount Titlis, Venice and the Vatican. "
          "Flights, visas, hotels, meals and sightseeing are all included.",
 'highlights': ['Bhaktivedanta Manor Sunday feast',
                'ISKCON Soho & Akshaya Patra',
                'Changing of the Guard · Koh-i-Noor',
                'Eiffel Tower, Louvre & Seine',
                'Radhadesh castle temple',
                'Keukenhof tulips · Amsterdam',
                'Goloka Dham · Black Forest',
                'Snow on Mount Titlis',
                'Lake Como · Venice gondola',
                'Vatican, Colosseum & Pisa'],
 'stays': [('London', '3 Nights'), ('Paris', '2 Nights'), ('Benelux', '2 Nights'),
           ('Germany', '2 Nights'), ('Switzerland', '2 Nights'), ('Italy', '4 Nights')],
 'best': 'Late April is spring: tulips at their peak, long evenings, 15–21 °C by day and 6–11 °C at night. '
         'Mount Titlis is below zero, so carry a warm jacket and gloves.',
 'stops': [('Hyderabad / Bangalore', 'Flights on 17 April', 'Flight', 'via Dubai / Abu Dhabi'),
           ('London', '3 nights · Manor · Tower · London Eye', 'Coach + ferry', 'Dover → Calais'),
           ('Paris', '2 nights · Eiffel Tower · Louvre · ISKCON Paris', 'Coach', '320 km'),
           ('Brussels & Radhadesh', 'Atomium · Grand Place · castle temple', 'Coach', '310 km'),
           ('Amsterdam', 'Canals · windmills · Keukenhof', 'Coach', '260 km'),
           ('Cologne & Goloka Dham', 'Cathedral · ISKCON Cologne · Sunday feast', 'Coach', '480 km'),
           ('Black Forest & Zurich', 'Titisee · Rhine Falls · ISKCON Zurich', 'Coach', '85 km'),
           ('Titlis, Lucerne & Interlaken', 'Snow · Lion Monument · lake cruise', 'Coach', '380 km'),
           ('Lake Como & Milan', 'Villaggio Hare Krishna · Duomo', 'Coach', '300 km'),
           ('Venice', 'Prabhupada Desh · Padova · gondola', 'Train', '4 h'),
           ('Rome, Vatican & Florence', "St Peter's · Colosseum · Villa Vrindavan", 'Coach', '300 km'),
           ('Pisa & Milan Malpensa', 'Leaning Tower · flights home on 2 May', '', '')],
 'journey_photos': [('towerbridge', 'Tower Bridge, London'), ('titlis', 'Mount Titlis, Switzerland'), ('venice', 'Venice, Italy')],
 'daypages': [
  {'n': 1, 'title': 'Fly to London · Kamada Ekadasi', 'stay': 'London (Wembley)', 'imgs': ['towerbridge', 'westminster'],
   'story': 'The Hyderabad group flies Emirates via Dubai and lands at Heathrow at 4:10 pm; the Bangalore group flies Etihad via '
            'Abu Dhabi and lands at 6:45 pm. Our tour manager meets both groups and takes them by coach to the hotel in Wembley. '
            'It is Kamada Ekadasi, so fruit meals are arranged on board. The day ends with a welcome kirtan and dinner.',
   'sig': ('Did you know?', 'Srila Prabhupada first came to London in 1969, and from London the Hare Krishna movement spread across '
           'Europe. Our yatra follows that path.')},
  {'n': 2, 'title': 'Akshaya Patra · Bhaktivedanta Manor · Soho', 'stay': 'London (Wembley)', 'imgs': ['manor', 'londoneye'],
   'story': "Visit the Akshaya Patra kitchen in Watford, then Bhaktivedanta Manor for darshan of Sri Sri Radha-Gokulananda, the "
            "Sunday programme and feast prasadam. In the afternoon, Madame Tussauds; in the evening, arati at ISKCON Soho and a "
            "stroll through Covent Garden.",
   'sig': ('Sacred significance', 'George Harrison gave Bhaktivedanta Manor to ISKCON in 1973. Srila Prabhupada stayed and '
           'translated there, and Radha-Londonishvara at Soho were the first ISKCON deities installed in the UK (1969).')},
  {'n': 3, 'title': 'Royal London', 'stay': 'London (Wembley)', 'imgs': ['guard', 'tower'],
   'story': "The Changing of the Guard at Buckingham Palace and The King's Gallery; the Tower of London with the Crown Jewels and "
            "the Koh-i-Noor; a walk on Tower Bridge; a Thames boat ride to the London Eye at sunset; then Big Ben and the Houses "
            "of Parliament.",
   'sig': ('Did you know?', 'The Koh-i-Noor came from the Kollur mines on the banks of the Krishna river in present-day Andhra '
           'Pradesh. It is now set in a crown kept in the Jewel House at the Tower of London.')},
  {'n': 4, 'title': 'London → Dover → ferry → Paris', 'stay': 'Paris', 'imgs': ['dover', 'arc'],
   'story': 'Coach to Dover and the ferry across the English Channel past the White Cliffs, then on through northern France to '
            'Paris, with kirtan and the pastimes of Lord Balarama on the way for Balarama Rasayatra.',
   'sig': ('On the way', 'At Dover, every yatri gives fingerprints and a photo for the new EU entry system. Our team plans '
           'extra time so the group is never rushed.')},
  {'n': 5, 'title': 'Paris: Eiffel Tower · Notre-Dame · ISKCON Paris', 'stay': 'Paris', 'imgs': ['eiffel', 'notredame'],
   'story': 'The Arc de Triomphe and the Champs-Élysées, the Eiffel Tower to the 2nd floor, South Indian lunch, Notre-Dame '
            'Cathedral, darshan and evening arati at ISKCON Paris, and a night cruise on the Seine past the lit-up city.',
   'sig': ('Did you know?', 'Srila Prabhupada visited Paris several times in the 1970s and spoke with French students and '
           'philosophers about the science of the soul.')},
  {'n': 6, 'title': 'Louvre → Brussels', 'stay': 'Brussels', 'imgs': ['louvre', 'grandplace'],
   'story': 'A guided morning at the Louvre to see the Mona Lisa and other masterpieces, then on to Belgium: the Atomium, the '
            'Grand Place with its golden guild houses, and Manneken Pis.',
   'sig': ('Did you know?', "Brussels' Grand Place is a UNESCO World Heritage Site and is often called one of the most "
           'beautiful squares in the world.')},
  {'n': 7, 'title': 'Radhadesh → Amsterdam', 'stay': 'Amsterdam', 'imgs': ['radhadesh', 'amsterdam'],
   'story': "Darshan, prasadam and a walk in the gardens at ISKCON Radhadesh, a castle temple in the Ardennes hills, then on to "
            "Amsterdam for an evening cruise on the UNESCO canal ring.",
   'sig': ('Sacred significance', "Radhadesh, in the Château de Petite Somme, is home to Sri Sri Radha-Gopinatha and is "
           "ISKCON's main temple and college for the Benelux countries.")},
  {'n': 8, 'title': 'Windmills & Keukenhof tulips → Cologne', 'stay': 'Cologne', 'imgs': ['keukenhof', 'windmills'],
   'story': 'The working windmills of Zaanse Schans, then the Keukenhof gardens at peak tulip season, then the drive to Cologne '
            'and an evening walk to the floodlit cathedral.',
   'sig': ('Did you know?', 'Keukenhof plants about seven million bulbs each year and opens for only eight weeks in spring. '
           'Late April is the best time to see it.')},
  {'n': 9, 'title': 'Cologne · Goloka Dham → Black Forest', 'stay': 'Titisee (Black Forest)', 'imgs': ['cologne', 'cologne2'],
   'story': "Cologne Cathedral and ISKCON Cologne, then the Sunday programme and feast at Goloka Dham, ISKCON's rural centre in "
            "Germany, and on to the Black Forest for the night.",
   'sig': ('Sacred significance', 'Goloka Dham is a peaceful farm community in the hills near Trier, where devotees live simply, protect '
           'cows and serve the deities.')},
  {'n': 10, 'title': 'Titisee · Rhine Falls → Zurich', 'stay': 'Zurich', 'imgs': ['rhinefalls', 'rhinefalls2'],
   'story': "Lake Titisee and the Black Forest cuckoo-clock shops, the thundering Rhine Falls, an orientation of Zurich's old "
            "town, then darshan, arati and kirtan with the Swiss devotees at ISKCON Zurich.",
   'sig': ('Did you know?', 'The Rhine Falls is the largest waterfall in Europe by volume, and it is at its strongest in spring '
           'when the Alpine snow melts.')},
  {'n': 11, 'title': 'Mount Titlis · Lucerne → Interlaken', 'stay': 'Interlaken', 'imgs': ['titlis', 'lucerne'],
   'story': "Up Mount Titlis by the revolving Rotair cable car for snow, the glacier cave and the Alpine views; Lucerne's Lion "
            "Monument and Chapel Bridge; a one-hour lake cruise; and a scenic train to Interlaken.",
   'sig': ('Did you know?', 'The Rotair was the first revolving cable car in the world. It turns a full circle on the way up '
           'to 3,020 m.')},
  {'n': 12, 'title': 'Interlaken → Lake Como → Milan', 'stay': 'Milan', 'imgs': ['titlis2', 'lucerne2'],
   'story': 'A morning view of the snowy Jungfrau, then through the Alps by the Gotthard to Italy: a boat ride on Lake Como and '
            'darshan, arati and kirtan at Villaggio Hare Krishna.',
   'sig': ('Sacred significance', "Villaggio Hare Krishna is ISKCON's oldest farm community in Italy, a village of devotees "
           'in the hills near Bergamo.')},
  {'n': 13, 'title': 'Milan Duomo · Prabhupada Desh · Venice', 'stay': 'Venice-Mestre', 'imgs': ['venice', 'venice2'],
   'story': "Milan's great cathedral, prasadam at ISKCON Prabhupada Desh, the Basilica of St Anthony in Padova, and an evening "
            "in Venice: St Mark's Square and a gondola ride.",
   'sig': ('Sacred significance', 'Prabhupada Desh is a devotee community in the Berici hills near Vicenza, named in honour of '
           'Srila Prabhupada.')},
  {'n': 14, 'title': 'Rome & the Vatican by high-speed train', 'stay': 'Florence', 'imgs': ['vatican', 'colosseum'],
   'story': "An early high-speed train to Rome: the Vatican Museums and the Sistine Chapel with licensed guides, St Peter's "
            "Basilica, the Colosseum and the Trevi Fountain, then the train to Florence for the night.",
   'sig': ('Did you know?', 'The Vatican is the smallest country in the world, and the eighth country on our yatra.')},
  {'n': 15, 'title': 'Florence · Villa Vrindavan · Pisa', 'stay': 'Near Milan Malpensa airport', 'imgs': ['pisa', 'pisa2'],
   'story': "Florence's Duomo, Piazza della Signoria and Ponte Vecchio, the panorama from Piazzale Michelangelo, prasadam at "
            "ISKCON Villa Vrindavan, and the Leaning Tower of Pisa, then a farewell dinner near Milan Malpensa.",
   'sig': ('Sacred significance', 'Villa Vrindavan is a 16th-century Tuscan villa among vineyards, home to a thriving '
           'community of devotees.')},
  {'n': 16, 'title': 'Flights home · Varuthini Ekadasi', 'stay': None, 'imgs': ['towerbridge', 'titlis'],
   'story': 'After an early breakfast, the group checks in at Milan Malpensa for Etihad via Abu Dhabi, landing in Hyderabad and '
            'Bangalore early on Monday 3 May. It is Varuthini Ekadasi, so fruit meals are arranged on board.',
   'sig': ('Parting prayer', 'We return home carrying the memories of the holy places, the association of devotees and the '
           'mercy of Srila Prabhupada, who brought Krishna to every town and village of the world.')}],
 'places': [('manor', 'Bhaktivedanta Manor', "Srila Prabhupada's home in England"),
            ('radhadesh', 'Radhadesh, Belgium', 'ISKCON castle temple in the Ardennes'),
            ('towerbridge', 'Tower Bridge, London', 'Thames boat ride and the Tower'),
            ('eiffel', 'Eiffel Tower, Paris', 'Up to the 2nd floor'),
            ('keukenhof', 'Keukenhof, Netherlands', 'Tulips at their spring peak'),
            ('titlis', 'Mount Titlis', 'Snow at 3,020 m'),
            ('venice', 'Venice', "Gondola ride and St Mark's"),
            ('vatican', "St Peter's, Vatican", 'Vatican Museums & Sistine Chapel'),
            ('pisa', 'Pisa', 'The Leaning Tower and Square of Miracles')],
 'incl': ['International flights from Hyderabad or Bangalore (economy, group fares)',
          'UK and Schengen visa charges',
          '15 nights in hotels, twin sharing',
          'All meals – pure-vegetarian sattvic prasadam, no onion or garlic; Ekadasi meals',
          'Private coach throughout, Dover–Calais ferry, all boats and the Swiss and Italian trains in the plan',
          'All sightseeing and entry tickets in the itinerary',
          'Experienced tour manager and licensed local guides',
          'Daily kirtan, japa and sthala purana with temple devotees'],
 'excl': ['GST 5% and TCS 2%', 'Personal expenses and shopping', 'Anything not listed under inclusions'],
 'flights': ['Hyderabad group: Emirates via Dubai, Sat 17 April, landing Heathrow 4:10 pm',
             'Bangalore group: Etihad via Abu Dhabi, Sat 17 April, landing Heathrow 6:45 pm',
             'Return: Etihad from Milan Malpensa via Abu Dhabi, Sun 2 May; landing Mon 3 May'],
 'flights_title': 'Flights · booked by us',
 'meal_note': 'All breakfasts, lunches and dinners are included: pure-vegetarian sattvic prasadam with no onion or garlic, '
              'at hotels, temples and selected Indian restaurants. Fruit meals on both Ekadasi travel days.',
 'why': [('Sattvic food', 'Pure-vegetarian prasadam every day, no onion or garlic, at hotels, temples and Indian restaurants'),
         ('Pre-approved stays', 'Hotels checked and approved by Punya Kshetras, not booked blind'),
         ('Comfortable transport', 'One private coach with experienced drivers, plus ferry, boats and trains'),
         ('Care for seniors', 'Seats near the front, lifts and wheelchairs where needed, unhurried pace'),
         ('Narration by devotees', 'Sthala purana and the glories of each holy place, in Telugu, Hindi and English'),
         ('Family-like yatra', 'Kirtan, japa and satsang every day with ISKCON Hare Krishna devotees'),
         ('No hidden charges', 'All-inclusive: flights, visas, stays, meals, tickets and transfers in one clear price')],
 'extra_terms': [('Visas', 'UK and Schengen visas are applied for by each yatri with our help; the visa fees are included. '
                  'Please give us your documents on time. If a visa is refused, the cancellation terms apply to the costs '
                  'already paid to airlines and hotels.'),
                 ('Flights & connections', 'Flights are booked on group fares and cannot be changed. If an airline, train '
                  'or ferry changes its schedule or a strike affects travel, our team will arrange the best alternative.')],
 'faq_common': [('What do I need for the visa?', 'A passport valid 3+ months after 3 May 2027 with 2 blank pages, Schengen-size '
                 'photos, income-tax returns, bank statements and a covering letter. We guide you through every step.'),
                ('What food is served?', 'Pure-vegetarian sattvic prasadam throughout, no onion or garlic, and fruit meals on '
                 'Ekadasi.')],
 'faq': [('How much walking is there?', 'City days have 10,000–15,000 steps at an easy pace. The coach drops us close to each '
          'place, and lifts are used wherever available.'),
         ('Will my phone work?', 'Take an international roaming pack or a Europe + UK eSIM. Check that Switzerland is covered.')],
 'pack': ['Passport, visa copies, photo ID',
          'Warm jacket, gloves, woollen cap',
          'Walking shoes already broken in',
          'Raincoat or umbrella',
          'Personal medicines with prescriptions',
          'Universal plug adapter, power bank',
          'Ekadasi snacks for 17 April and 2 May'],
 'dos': ['Carry your passport on travel days',
         'Be at the coach 5 minutes early',
         'Dress modestly for churches and the Vatican',
         'Use the buddy system; keep your phone charged',
         'Keep coins for toilets (€0.50–€1)',
         'Drink plenty of water'],
 'donts': ["Don't carry valuables in back pockets",
           "Don't accept 'free' bracelets or roses",
           "Don't leave the group without telling the leader",
           "Don't take meat, dairy or fresh produce into the UK/EU",
           "Don't buy from street sellers near monuments",
           "Don't take photos where signs prohibit it"],
 'back': 'venice',
 'closing': 'Hare Krishna!',
 'rows': 'rows.json',
 'poster': {'hero': 'towerbridge', 'pos': '50% 40%', 'circ': ['manor', 'eiffel', 'titlis'],
            'kicker': '8 Countries · 10 ISKCON Temples',
            'price_small': '+ 5% GST + 2% TCS · per person · incl. international flights',
            'hl': ['International flights & visas included',
                   'Bhaktivedanta Manor & ISKCON Soho',
                   '10 ISKCON temples across Europe',
                   'Tower of London & London Eye',
                   'Eiffel Tower, Louvre & Seine cruise',
                   'Keukenhof tulips & Amsterdam canals',
                   'Snow on Mount Titlis · Venice · Vatican',
                   'Sattvic prasadam · kirtan every day']},
}
