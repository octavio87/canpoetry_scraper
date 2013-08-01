#Canadian Poetry Web Scraper v0.1
#Uses BeautifulSoup and urllib2 libraries
#Install them before running the scraper
from bs4 import BeautifulSoup
import urllib2
import re
#List of Canadian and English publishers 
#compiled from http://canlit.ca/publishers, http://en.wikipedia.org/wiki/List_of_English_language_book_publishers, 
bookpublishers=['Algonquin Books', 'Arte Publico Press', 'Atlantic Books', 'Bellevue Literary Press', 'Blackwell Publishers', 'Coffee House Press','Dryad Press','Faber and Faber','Four Walls Eight Windows','Graywolf Press','Mercury House','Milkweed Editions','New Rivers Press','Picador','Sarabande Books','Small Beer Press','Southwick House','Tarpaulin Sky Press','TSAR Publications','Turnstone Press','Two Dollar Radio','Washington Writers Publishing House','Vrzhu Press','vanity press', 'Abilene Christian University Press', 'Ablex Publishing', 'Elsevier', 'Ace Books', 'Penguin Group', 'Academic Press', 'Elsevier', 'Addison\xe2\x80\x93Wesley', 'Pearson Education', 'Adis International', 'Wolters Kluwer', 'Akashic Books', 'Aladdin Publisher|Aladdin Paperbacks', 'imprint', 'Simon & Schuster', 'Allen & Unwin', 'Alyson Books', 'Andr\xc3\xa9 Deutsch', 'Carlton Publishing Group', 'Andrews McMeel Publishing', 'Anova Books', 'Anvil Press Poetry', 'Applewood Books', 'Apress', 'Arbor House', 'Arcade Publishing', 'Arcadia Publishing', 'Airiti Press', 'Airiti Inc', 'Arkham House', 'Armida Publications', 'ArtScroll', 'A. S. Barnes', 'Alfred Smith Barnes', 'Athabasca University Press', 'Atheneum Books', 'Simon & Schuster', 'Atheneum Publishers', 'Atlantic Books', 'Atlas Press', 'ATOM Books', 'Little, Brown', 'Augsburg Fortress', 'Evangelical Lutheran Church in America', 'Aunt Lute Books', 'Avon (publishers)|Avon Publications', 'HarperCollins', 'B & W Publishing', 'Baen Books', 'Baker Book House', 'Banner of Truth Trust', 'Barrie & Jenkins', 'Basic Books', 'Ballantine Books', 'Bantam Books', 'Random House', 'Bantam Spectra', 'Bantam Books', 'BBC Books', 'Harvard University Press|Belknap Press', 'Bella Books', 'Bellevue Literary Press', 'Berg Publishers', 'Bloomsbury Publishing Plc', 'Berkley Books', 'imprint', 'Springer Science+Business Media', 'Bison Books', 'A & C Black', 'Bloomsbury Publishing Plc', 'Black Dog Publishing', 'Black Library', 'Black Sparrow Books', 'Blackie and Son Limited', 'Blackwell Publishing', 'John Blake Publishing|Blake Publishing', 'Bloodaxe Books', 'Bloomsbury Publishing Plc', 'Blue Ribbon Books', 'Bobbs-Merrill Company', 'Howard W. Sams Company', 'Book League of America', 'Book Works', 'Borgo Press', 'Wildside Press', 'Boundless (company)|Boundless', 'Bowes & Bowes', 'Marion Boyars Publishers', 'Boydell & Brewer', 'Broadview Press', 'Breslov Research Institute', 'Brill Publishers', 'Brimstone Press', 'Burns & Oates', 'Continuum International Publishing Group', 'Butterworth-Heinemann', 'Elsevier', 'Caister Academic Press', 'Cambridge University Press', 'Candlewick Press', 'Canongate Books', 'Carcanet Press', 'Carlton Books', 'Carlton Publishing Group', 'Carnegie Mellon University Press', 'Casemate Publishers', 'Orion Publishing Group|Cassell', 'Cengage Learning', 'Central European University Press', 'Century (imprint)|Century', 'Random House', 'Chambers Harrap', "Charles Scribner's Sons", 'Chatto and Windus', 'Chick Publications', 'Chronicle Books', 'Churchill Livingstone', 'Elsevier', 'City Lights Publishers', 'Cloverdale Corporation', 'Cold Spring Harbor Laboratory Press', "Collector's Guide Publishing", 'HarperCollins|Collins', 'Columbia University Press', 'Concordia Publishing House', 'Constable & Co Ltd', 'Constable & Robinson', 'Continuum International Publishing Group', 'Copper Canyon Press', 'Cork University Press', 'Cornell University Press', 'Coronet Books', 'Hodder & Stoughton', 'Craftsman Book Company', 'CRC Press', 'Crocker & Brewster', 'Crown Publishing Group', 'Random House', 'Da Capo Press', 'Perseus Books Group', 'Daedalus Publishing', 'Dalkey Archive Press', 'Darakwon Press', 'David & Charles', 'DAW Books', 'Donald A. Wollheim', 'Dedalus Books', 'Del Rey Books', 'Random House', 'Delacorte Press', 'Random House', 'J. M. Dent', 'Dick and Fitzgerald', 'Directmedia Publishing', 'DNA Publications', 'Dodd, Mead and Company', 'Dorchester Publishing', 'Dorling Kindersley', 'Doubleday (publisher)|Doubleday', 'Random House', 'Douglas & McIntyre', 'Dove Medical Press', 'Dover Publications', 'Dundurn Group', 'E. P. Dutton', 'Penguin Group', 'Earthscan', 'ECW Press', 'Eel Pie Publishing', 'Eerdmans Publishing', "Ellora's Cave", 'Elsevier', 'Reed Elsevier', 'Emerald Group Publishing', 'Europa Press', "Everyman's Library", 'Ewha Womans University Press', 'Exact Change', 'Faber and Faber', 'FabJob', 'Fairview Press', 'Farrar, Straus & Giroux', 'Henry Holt and Company', 'Fearless Books', 'Felony & Mayhem Press', 'Firebrand Books', 'Flame Tree Publishing', 'Llewellyn Worldwide', 'Focal Press', 'Folio Society', 'Forum Media Group', 'Four Courts Press', 'Four Walls Eight Windows', 'Free Press (publisher)|Free Press', 'Frederick Fell Publishers, Inc.', 'Frederick Warne & Co', 'Fulcrum Press', 'Funk & Wagnalls', 'G-Unit Books', 'Gaspereau Press', "Gay Men's Press", 'George Newnes', 'Gefen Publishing House', 'George Routledge & Sons', 'Victor Gollancz Ltd', 'Good News Publishers', 'Goops Unlimited', 'Goose Lane Editions', 'Golden Cockerel Press', 'Grafton (publisher)|Grafton', 'Graywolf Press', 'Greenleaf Book Group', 'Greenery Press', 'Greenwillow Books', 'HarperCollins', 'Greenwood Publishing Group', 'Gregg Press', 'Grosset & Dunlap', 'Grove Press', 'Atlantic Monthly Press', 'Hachette Book Group USA', 'Hackett Publishing Company', 'Happy House', 'Darakwon Press', 'Hamish Hamilton', 'Penguin Books', 'Harcourt Trade Publishers', 'Harcourt Assessment', 'Harlequin Enterprises Ltd', 'Harper & Brothers', 'Harper & Row', 'HarperCollins', 'HarperPrism', 'HarperCollins', 'HarperTrophy', 'HarperCollins', 'Harry N. Abrams, Inc.', 'Harvard University Press', 'Harvest House', 'Harvill Press at Random House', 'Hawthorne Books', 'Hay House', 'Haynes Manuals', 'Heinemann (book publisher)|Heinemann', 'Harcourt Education', 'Reed Elsevier', 'Herbert Jenkins Ltd|Herbert Jenkins', 'Heyday Books', 'HMSO', 'Hodder & Stoughton', 'Hodder Headline', 'Hogarth Press', 'Holland Park Press', 'Holt McDougal', 'Hoover Institution|Hoover Institution Press', 'Horizon Scientific Press', 'Houghton Mifflin', 'House of Anansi Press', 'The House of Murky Depths', 'Howell-North Books', 'Humana Press', 'Hutchinson (publisher)|Hutchinson', 'Hyperion (publisher)|Hyperion', 'Ian Allan Publishing', 'Brill Publishers', 'Ignatius Press', 'Imperial War Museum', 'Indiana University Press', 'Informa Healthcare', 'Information Age Publishing', 'Insomniac Press', 'International Universities Press', 'Inter-Varsity Press', 'InterVarsity Press', 'International Association of Engineers', 'Ishi Press', 'Island Press', 'Ivyspring International Publisher', 'Jaico Publishing House', 'Jarrolds Publishing', 'Jarrolds', 'John Murray (publisher)|John Murray', 'John Wiley & Sons', 'Jones and Bartlett Learning', 'Kehot Publication Society', 'Kessinger Publishing', 'Springer Science+Business Media|Kluwer Academic Publishers', 'Alfred A. Knopf', 'Kodansha', 'Kumarian Press', 'Karadi Tales', 'Ladybird Books', 'Leaf Books', 'Leafwood Publishers', 'Abilene Christian University Press', 'Left Book Club', 'Legas', 'Legend Books', 'Random House', 'Lethe Press', 'Libertas Academica', 'Liberty Fund', 'Library of America', 'LifeBound', 'Lion Hudson', 'Lion Publishing', 'Lion Hudson', 'Little, Brown and Company', 'Liverpool University Press', 'Llewellyn Worldwide', 'Longman', 'LPI Media', 'Lutterworth Press', 'Lippincott Williams & Wilkins', 'Wolters Kluwer', 'A. C. McClurg', 'McClelland and Stewart', 'Macmillan Publishers', 'Mainstream Publishing', 'Manning Publications', 'Mandrake of Oxford', 'Mandrake Press', 'Manchester University Press', 'Manor House Publishing', 'Mapin Publishing', 'Marion Boyars Publishers', 'Mark Batty Publisher', 'Marshall Cavendish', 'Marshall Pickering', 'HarperCollins', 'Martinus Nijhoff Publishers', 'Brill Publishers', 'Mascot Books', 'Matthias Media', 'McGraw-Hill', 'Medknow Publications', 'Melbourne University Publishing', 'Methuen Publishing', 'Michael Joseph (publisher)|Michael Joseph', "Michael O'Mara Books", 'Michigan State University Press', 'Microsoft Press', 'Microsoft', 'The Miegunyah Press', 'Miles Kelly Publishing', 'Mills & Boon', 'Minerva Press', 'Mirage Publishing', 'MIT Press', 'Mkuki na Nyota', 'Modern Library', 'Mother Tongue Publishing', 'John Murray (publisher)|John Murray', 'Mycroft & Moran', 'Arkham House', 'Naiad Press', 'Nauka (publisher)|Nauka', 'NavPress', 'New Directions Publishing', 'New English Library', 'New Holland Publishers', 'The New Press', 'New Village Press', 'George Newnes|Newnes', 'Nonesuch Press', 'Noontide Press', 'Northwestern University Press', 'W. W. Norton & Company', 'NRC Research Press', 'NYRB Classics', 'Oberon Books', 'Open University Press', 'Orchard Books', 'McGraw Hill', 'Orion Books', 'Orion Publishing Group', "O'Reilly Media", 'McGraw Hill', 'Osprey Publishing', 'Other Press', 'Peter Owen Publishers', 'Oxford University Press', 'Palgrave Macmillan', 'Pan Books', 'Pan Macmillan', 'Pantheon Books at Random House', 'Parachute Publishing', 'Parragon', 'Pathfinder Press', 'Paulist Press', 'Pavilion Books', 'Peace Hill Press', 'Pecan Grove Press', 'Pen and Sword Books', 'Penguin Books', 'Penguin Putnam Inc.', 'Penn State University Press', 'Persephone Books', 'Perseus Books Group', 'Peter Lang (publishing company)|Peter Lang', 'Peter Owen Publishers', 'Phaidon Press', 'Philosophy Documentation Center', 'Philtrum Press', 'Picador (imprint)|Picador', 'Pimlico Books at Random House', 'Pluto Press', 'Point Blank', 'Wildside Press', 'Poisoned Pen Press', 'The Policy Press', 'Polity', 'Practical Action', 'Prentice Hall', 'Prime Books', 'Princeton University Press', 'Progress Publishers', 'Prometheus Books', 'Profile Books', 'Puffin Books', 'Penguin Books', "G. P. Putnam's Sons", 'Que Publishing', 'Quebecor', 'Quirk Books', 'Random House', 'Realtime Publishers', 'Reed Elsevier', 'D. Reidel', 'Springer Science+Business Media', 'Remington & Co', 'Research Publishing Services', 'Harcourt Education', 'Reed Elsevier', 'Riverhead Books', 'Robson Books', 'Rock scorpion books', 'Rodopi Publishers|Rodopi', 'Routledge|Routledge Kegan Paul', 'Routledge', 'Taylor & Francis', 'Rowman & Littlefield', 'Royal Society of Chemistry', 'SAGE Publications', 'Sams Publishing', "St. Martin's Press", 'Salt Publishing', 'Schocken Books', 'Scholastic Press', "Charles Scribner's Sons|Scribner", 'Secker & Warburg', 'Shambhala Publications', 'Shire Books', 'Shoemaker & Hoard Publishers', 'Shuter & Shooter Publishers', 'Sidgwick & Jackson', 'Signet Books', 'New American Library', 'Simon and Schuster', 'Sinclair-Stevenson Ltd', 'Sounds True', 'Sourcebooks', 'South End Press', 'SPCK', "Spinster's ink books", 'Eyre & Spottiswoode', 'Springer Science+Business Media', 'Stanford University Press', 'The Stationery Office', 'Stein and Day', 'Summerwild Productions', 'Summit Media', 'SUNY Press', 'Sussex Academic Press', 'T & T Clark', 'Tachyon Publications', 'Tammi (publishing company)|Tammi', 'Target Books', 'Tarpaulin Sky Press', 'Tartarus Press', 'Taunton Press', 'Taylor & Francis', 'Ten Speed Press', 'Thames & Hudson', 'Thames & Hudson USA', 'The Good Book Company', 'Thieme Medical Publishers', 'Third World Press', 'Thomas Nelson (publisher)|Thomas Nelson', 'Ticonderoga Publications', 'Times Books', 'Titan Books', 'Tor Books', 'Triangle Books', 'SPCK', 'Malcolm Whyte|Troubador Press', 'Tupelo Press', 'Tuttle Publishing', 'Twelveheads Press', 'UCL Press', 'Unfinished Monument Press', 'University of Akron Press', 'University of Alaska Press', 'University of California Press', 'University of Chicago Press', 'University of Minnesota Press', 'University of Michigan Press', 'University of Nebraska Press', 'University of Pennsylvania Press', 'University of South Carolina Press', 'University of Toronto Press', 'University of Wales Press', 'University Press of America', 'University Press of Kansas', 'University Press of Kentucky', 'Usborne Publishing', 'Verso Books', 'Velazquez Press', 'Viking Press', 'Vintage Books', 'Vintage Books at Random House', 'Virago Press', 'Virgin Publishing', 'Voyager Books', 'HarperCollins', 'Brill Publishers', 'W. W. Norton & Company', 'Ward Lock & Co', 'WBusiness Books', 'WEbook', 'Weidenfeld & Nicolson', 'Wesleyan University Press', 'WestBow Press', 'Thomas Nelson (publisher)|Thomas Nelson', 'W. H. Allen Ltd', 'Wildside Press', 'William Edwin Rudge', 'Windgate Press', 'Wipf and Stock', 'Wisdom Publications', 'Woodhead Publishing', 'Workman Publishing', 'World Publishing Company', 'World Scientific Publishing', 'Wrecking Ball Press', 'Wrox Press', 'John Wiley & Sons', 'Sanoma|WSOY', 'John Wiley & Sons', 'Xoanon Publishing', 'Yale University Press', 'Zed Books', 'Ziff Davis Media', 'Zondervan','8th House Publishing', 'ABC Publishing (Anglican Book Centre)', 'Academic Printing and Publishing', 'Acadiensis Press', 'Acorn Press Canada', 'Alcuin Society, The', 'Amethyst House Publishing Inc.', 'Anchor Canada', 'Annick Press', 'Anvil Press Publishers', 'Aquila Communications Inc.', 'Arbeiter Ring Publishing', 'Arsenal Pulp Press', 'Artistic Warrior', 'Association of Book Publishers of British Columbia (ABPBC)', 'Association of Manitoba Book Publishers (AMBP)', 'Asteroid Publishing Inc.', 'Athabasca University Press', 'Augustine Hand Press', 'Banff Centre Press', 'Between the Lines', 'Biblioasis', 'Black Moss Press', 'Blue Gamma Publishers Corp.', 'Blue Heron Press', 'Book Publishers Association of Alberta (BPAA)', 'BookLand Press', 'Borealis Press', 'Breakwater Books Ltd.', 'Brick Books', 'Brindle & Glass', 'Broadview Press', 'Broken Jaw Press Inc.', 'BuschekBooks', 'Cambridge University Press Canada', "Canadian Educators' Press", 'Canadian Museum of Civilization', 'Canadian Plains Research Centre', "Canadian Scholars' Press", 'Cape Breton Catalogue', 'Cape Breton University Press', 'Clark-Nova Books', 'Coach House Books', 'Commodore Books', "Commoners' Publishing Society Inc.", 'Cormorant Books', 'Coteau Books', 'Creative Book Publishing', 'Creative Bound Inc.', 'D&M Publishers Inc.', 'Deux Voiliers Publishing', 'Douglas Gibson Books (McClelland & Stewart Ltd.)', 'Drawn and Quarterly', 'Drawspace', 'DreamCatcher Publishing', 'Dundurn Group', 'ECW Press', 'Ekstasis Editions', 'Emblem Editions (McClelland & Stewart)', 'emc notes, inc.', 'Ergo Books', 'Fernwood Publishing', 'Fifth House Publishers', 'Flanker Press', 'Folklore Publishing', 'Frog Hollow Press', 'Frontenac House', 'Gaspereau Press', 'General Store Publishing House', 'Gerbil Meets Mouse Publishing', 'Goose  Lane Editions', 'Granville Island Publishing', 'Great Plains Publications', 'Groundwood Books', 'Gu\xc3\x83\xc2\xa9rin \xc3\x83?diteur Lt\xc3\x83\xc2\xa9e', 'Guernica Editions', 'GWEV Publishing Inc.', 'Hagios Press', 'Harbour Publishing', 'HarperCollins Canada', 'Hedgerow Press', 'House of Anansi Press', 'House of Parlance', 'Hungry I Books', 'Inanna Publications and Education Inc.', 'Inscape Publications', 'Insomniac Press', 'Intl Self-Counsel Press', 'James Lorimer & Company', 'Kegedonce Press', 'Key Publishing House, The', 'Kids Can Press Ltd.', 'Leaf Press', 'Left Field Press', 'Les \xc3\x89ditions Adage', 'Les \xc3\x89ditions David', 'Les \xc3\x89ditions du Bor\xc3\xa9al', 'Les \xc3\x89ditions du CRAM', "Les Presses de l'Universit\xc3\x83\xc2\xa9 d'Ottawa - University of Ottawa Press", 'Librarie Sigogne', 'littlefishcartpress', 'Lobster Press', 'Loon Books', 'Loon in Balloon Inc.', 'Maa Press', 'Mansfield Press', 'Maple Tree Press', 'McClelland & Stewart', "McGill-Queen's University Press", 'McGilligan Books', 'Mercury Press, The', 'Moon Willow Press', 'Mother Tongue Press', 'New World Publishing', 'NeWest Press', 'Nightwood Editions', 'Nimbus Publishing Ltd.', 'Norwood Publishing Ltd.', 'Now Or Never Publishing', 'Oberon Press', 'Oolichan Books', 'Orca Book Publishers', 'Oxford University Press Canada', 'Paper Birch Publishing', 'Pedlar Press', 'Pembroke Publishers Limited', 'Pemmican Publications Inc.', 'Penumbra Press', 'Playwrights Canada Press', "Porcupine's Quill", 'Pottersfield Press', "Presses de l'Universit\xc3\x83\xc2\xa9 de Montr\xc3\x83\xc2\xa9al", 'Purich Publishing Ltd.', 'Qualitas Publishing', 'Quattro Books', 'QWERTY', 'Rainbird Press', 'Raincoast Books', 'Rattling Books', 'Rocky Mountain Books', 'Ronsdale Press', 'Saskatchewan Publishers Group (SPG)', 'Scroll Press', 'Second Story Press', 'Seraphim Editions', 'Short Sharp Stock', 'Signal Editions', 'Signature Editions', 'Sono Nis Press', 'Spotted Cow Press', "St. John's College Press", 'Stationaery Press', 'Sumach Press', 'Sybertooth Inc.', 'Talon Books', 'The Alfred Gustav Press', 'The Book Room', 'The Boston Mills Press', 'The Ginger Press', 'Theytus Books', 'Thistledown Press Ltd.', 'Thomas Allen & Sons Ltd.', "Three O'Clock Press", 'Totem Pole Books', 'TouchWood Editions', 'Tradewind Books', 'Trafford Publishing', 'Trillistar Books', 'TSAR Publications', 'Tundra Books', 'Turnstone Press', 'Umberto Press', 'University Extension Press (U of Saskatchewan)', 'University of Alberta Press', 'University of British Columbia Press', 'University of Calgary Press', 'University of Manitoba Press', 'University of Northern British Columbia Press', 'University of Saskatchewan Press', 'University of Toronto Press', 'University of Western Ontario Publications', 'V\xc3\xa9hicule Press', 'Vintage Canada', 'Wattle and Daub Books', 'Whitecap Books Ltd.', 'Wilfrid Laurier University Press', 'Wolsak and Wynn Publishers Ltd', "Women's Press", "Women's Press Literary", 'Wood Lake Books', 'XoXo Publishing (TM)', 'XYZ \xc3\x83?diteur / XYZ Publishing', 'York Press Ltd.', 'Your Scrivener Press', 'Zygote Publishing', 'MisFit', 'Ekstasis editions','Penguin', 'Douglas & McIntyre', 'The Mercury Press','Coach House Press', 'Aya Press', 'Dreadnaught Press', 'Unfinished Monument Press','Key Porter Books','Moonstone Press', 'Mosaic Press','Mosaic Press/Valley Editions','Oberon Press', 'Three Trees Press']

cities=['Victoria', 'Buenos Aires', 'Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Vienna', 'Baku/Sumqayit', 'Brussels', 'Antwerp', 'Sao Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Recife', 'Porto Alegre', 'Fortaleza', 'Curitiba', 'Campinas', 'Brasilia', 'Goiania', 'Phnom Penh', 'Santiago', 'Shanghai', 'Beijing', 'Shenzhen', 'Tianjin', 'Shenyang', 'Dalian', 'Bogota', 'Kinshasa', 'Lumumbashi', 'Copenhagen', 'Quito', 'Cairo', 'Helsinki', 'Paris', 'Marseille', 'Lyon', 'Lille', 'Nice', 'Toulouse', 'Bordeaux', 'Nantes', 'Toulon', 'Douai/Lens', 'Valenciennes', 'Tours', 'Bethune', 'Avignon', 'Pau', 'Essen', 'Berlin', 'Frankfurt', 'Cologne/Bonn', 'Hamburg', 'Munich', 'Stuttgart', 'Aachen', 'Accra', 'Athens', 'Budapest', 'Mumbai', 'Delhi', 'Kolkata', 'Chennai', 'Bangalore', 'Hyderabad', 'Jakarta', 'Tehran', 'Baghdad', 'Dublin', 'Tel Aviv', 'Milan', 'Rome', 'Naples', 'Turin', 'Tokio', 'Osaka/Kobe/Kyoto', 'Nagoya', 'Fukuoka', 'Sapporo', 'Kuwait', 'Beirut', 'Kuala Lumpur', 'Mexico City', 'Guadalajara', 'Monterey', 'Rotterdam', 'Auckland', 'Lagos', 'Karachi', 'Lahore', 'Lima', 'Manila', 'Katowice', 'Warsaw', 'Lisbon', 'Porto', 'San Juan', 'Aguadilla', 'Moscow', 'St Petersburg', 'Nizhni Novgorod', 'Riyadh', 'Jeddah', 'Damman ', 'Singapore', 'Johannesburg', 'East Rand', 'Durban', 'Cape Town', 'Pretoria', 'Port Elizabeth', 'Vereeniging', 'Seoul/Incheon', 'Madrid', 'Barcelona', 'Khartoum', 'Stockholm', 'Taipei', 'Taichung', 'Bangkok', 'Istanbul', 'Ankara', 'Dubai', 'Abu Dhabi', 'London', 'Birmingham', 'Manchester', 'Leeds/Bradford', 'Glasgow', 'Donetsk', 'New York', 'Los Angeles', 'Chicago', 'Philadelphia', 'Miami', 'Dallas', 'Boston', 'Washington', 'Detroit', 'Houston', 'Atlanta', 'San Francisco', 'Phoenix', 'Seattle', 'San Diego', 'Minneapolis', 'St. Louis', 'Baltimore', 'Tampa', 'Denver', 'Cleveland', 'Pittsburgh', 'Portland', 'San Jose', 'Riverside/San Bernardino', 'Cincinnati', 'Virginia Beach', 'Sacramento', 'Kansas City', 'San Antonio', 'Las Vegas', 'Milwaukee', 'Indianapolis', 'Providence', 'Orlando', 'Columbus', 'New Orleans', 'Buffalo', 'Memphis', 'Austin', 'Bridgeport', 'Stanford', 'Stamford', 'Salt Lake City', 'Jacksonville', 'Louisville', 'Hartford', 'Richmond', 'Charlotte', 'Nashville', 'Oklahoma City', 'Tucson', 'Honolulu', 'Dayton', 'Rochester', 'El Paso', 'Birmingham', 'Omaha', 'Albuquerque', 'Bethlehem', 'Allentown', 'Springfield', 'Akron', 'Albany', 'Sarasota//Bradenton', 'Tulsa', 'Concord', 'Raleigh', 'Grand Rapids', 'New Haven', 'McAllen', 'Toledo', 'Baton Rouge', 'Colorado Springs', 'Worcester', 'Charleston', 'Wichita', 'Columbia', 'Knoxville', 'Ogden', 'Youngstown', 'Syracuse', 'Palm Bay', 'Scranton', 'Flint', 'Harrisburg', 'Little Rock', 'Poughkeepsie', 'Chattanooga', 'Augusta', 'Spokane', 'Cape Coral', 'Lancaster', 'Pensacola', 'Mobile', 'Greenville', 'Winston', 'Jackson', 'Durham', 'Fayetteville', 'South Bend', 'Shreveport', 'Port St Lucie', 'Canton', 'Barnstable Town', 'Asheville', 'Bonita Springs ', 'Naples', 'Huntsville', 'Hickory', 'Tashkent', 'Ho Chi Minh City', 'Harare', 'La Tuque', 'Senneterre', 'Rouyn-Noranda', 'Halifax Regional Municipality', "Val-d'Or", 'Greater Sudbury', 'Kawartha Lakes', 'Timmins', 'Ottawa', 'Cape Breton Regional Municipality', 'Queens', 'Gillam', 'Sept-Iles', 'Norfolk County', 'Leaf Rapids', 'Haldimand County', 'Snow Lake', 'Saguenay', 'Gasp\xc3\xa9', 'Hamilton', 'Port-Cartier', 'Prince Edward County', 'Lynn Lake', 'County of Brant', 'Shawinigan', 'Calgary', 'T\xc3\xa9miscaming', 'Huntsville', 'Chibougamau', 'Elliot Lake', 'Caledon', 'Edmonton', 'Saint-Raymond', 'Laurentian Hills', 'Toronto', 'Bracebridge', 'Iroquois Falls', 'Mont-Laurier', 'Degelis', 'Belleterre', 'Baie-Saint-Paul', 'Cochrane', 'South Bruce Peninsula', 'Lakeshore', 'Kearney', 'Blind River', 'Gravenhurst', 'Mississippi Mills', 'Northeastern Manitoulin and the Islands', 'Quinte West', 'Mirabel', 'Fermont', 'Winnipeg', 'Greater Napanee', 'La Malbaie', 'Riviere-Rouge', 'Quebec', 'Quebec City', 'Kingston', 'Levis', "St. John's", 'Becancour', 'Perce', 'Amos', 'London', 'Chandler', 'Whitehorse', 'Gracefield', 'Baie Verte', 'Milton', 'Montreal', 'Saint-F\xc3\xa9licien', 'Abbotsford', 'Sherbrooke', 'Gatineau', 'Pohenegamook', 'Baie-Comeau', 'Thunder Bay', 'Plympton\xe2\x80\x93Wyoming', 'Surrey', 'Prince George', 'Saint John', 'North Bay', 'Happy Valley-Goose Bay', 'Minto', 'Kamloops', 'Erin', 'Clarence-Rockland', 'Cookshire-Eaton', 'Dolbeau-Mistassini', 'Trois-Rivieres', 'Mississauga', 'Georgina', 'The Blue Mountains', 'Innisfil', 'Essex', 'Mono', 'Halton Hills', 'New Tecumseth', 'Vaughan', 'La Tuque', 'Oakville', 'Stratford', 'Dundas', 'Peterborough', 'Oakland', 'Mesa', 'D\xc3\xbcsseldorf', 'Salem', 'St. Petersburg']

canpoetryAuthors={'Jay': 'Ruzesky', 'Barry': 'Dempster', 'Lesley': 'Choyce', 'Andrew': 'Steinmetz', 'Jan': 'Horner', 'Stephen': 'Morrissey', 'Anne': 'Michaels', 'Anna': 'Mioduchowska', 'Kathy': 'Shaidle', 'Afua': 'Cooper', 'Fred': 'Wah', 'Margaret': 'Avison', 'Jill': 'Battson', 'Christopher': 'Wiseman', 'Libby': 'Scheier', ('Wayne', 'Scott'): 'Ray', 'Louis': 'Dudek', 'Michael': 'Redhill', 'Alice': 'Major', 'Adeena': 'Karasick', 'Betsy': 'Struthers', 'Noah': 'Leznoff', 'Robyn': 'Sarah', 'Steven': 'Heighton', 'Paul': 'Vermeersch', ('Fiona', 'Tinwei'): 'Lam', 'Jeffery': 'Donaldson', 'George': 'Thaniel', 'Kevin': 'Irie', 'Marvyne': 'Jenoff', 'Glen': 'Sorestad', 'Fraser': 'Sutherland', 'Patricia': 'Young', 'Eddy': 'Yanofsky', ('Linda', 'M.'): 'Stitt', 'Ellen': 'Jaffe', 'Wendy': 'Morton', 'Jane': 'Urquhart', 'John': 'Terpstra', ('Jane', 'Eaton'): 'Hamilton', 'Bert': 'Almon', 'Elizabeth': 'Zetlin', 'Bruce': 'Meyer', 'Joy': 'Kogawa', 'Malca': 'Litovitz', 'Dave': 'Margoshes', 'A.M.': 'Klein', 'Joe': 'Rosenblatt', 'Rhona': 'McAdam', 'Susan': 'Stenson', 'Rudyard': 'Fearon', 'Bill': 'Howell', 'Dionne': 'Brand', 'David': 'Waltner-Toews', 'Stephanie': 'Bolster', 'Lorna': 'Crozier', 'Carolyn': 'Smart', 'Ron': 'Charach', 'Roo': 'Borson', 'Catherine': 'Graham', 'Elisabeth': 'Harvor', 'Jennifer': 'Footman', 'Laura': 'Lush', 'Karen': 'Shenfeld', 'Sandy': 'Shreve', ('Mary', 'di'): 'Michele', 'Robert': 'Sward', 'Gary': 'Hyland', 'Tom': 'Wayman', 'P.K.': 'Page', 'Harold': 'Rhenisch', 'R.M.': 'Vaughan', 'Earle': 'Birney', ('Margaret', 'Lindsay'): 'Holton', ('Carole', 'Glasser'): 'Langille', 'Stan': 'Rogal', 'Patrick': 'Friesen', 'Phil': 'Hall', 'E.J.': 'Pratt', ('D.', 'C.'): 'Reid', ('Simon', 'Joseph'): 'Ortiz', 'Sheila': 'Martindale', ('Maureen', 'Scott'): 'Harris', 'Sonnet': "L'Abb\xc3\xa9", 'Milton': 'Acorn', 'Kenneth': 'Sherman', 'Marianne': 'Bluger', 'Rhea': 'Tregebov', 'bill': 'bissett', ('Francis', 'Edward'): 'Sparshott', 'Peter': 'Christensen', ('Susan', 'L.'): 'Helwig', 'Alison': 'Pick', 'Pat': 'Lowther', ('J.', 'Hugh'): 'MacDonald', 'Richard': 'Stevenson', ('M.', 'E.'): 'Csamer', 'Douglas': 'Lochhead', 'Brian': 'Henderson', 'Edward': 'Gates', 'Linda': 'Rogers', 'Penn': 'Kemp', ('George', 'Elliott'): 'Clarke', 'Erin': 'Mour\xc3\xa9', ('F.', 'R.'): 'Scott', 'Molly': 'Peacock', 'Irving': 'Layton', ('John', 'Robert'): 'Colombo', 'Kim': 'Morrissey', 'Lionel': 'Kearns', 'Lynn': 'Crosbie', ('M.', 'Travis'): 'Lane', 'Don': 'Coles', 'Janis': 'Rapoport', 'Sky': 'Gilbert', ('John', 'B.'): 'Lee', ('David', 'W.'): 'McFadden', 'Rosemary': 'Sullivan', 'Sophia': 'Kaszuba', ('Peter', 'Dale'): 'Scott', ('Desi', 'Di'): 'Nardo', ('Armand', 'Garnet'): 'Ruffo', 'Julie': 'Berry', 'Al': 'Purdy', 'Sonja': 'Dunn', 'Gwendolyn': 'MacEwen', 'Dennis': 'Lee', 'Zachariah': 'Wells'}



def GetAuthorList(lname, fnamef):
    lnameURL=""
    print fnamef, lname
    if " " in fnamef:
       fname=fnamef.split(" ")
       if fname[1].lower()=="di" or fname[1].lower=="de":
          lnameURL=fname[1].lower()+lname.lower()
          lnamef = fname[1].title()+" "+lname
          fnamefinal = fname[0]
          url="http://www.library.utoronto.ca/canpoetry/"+fname[1].lower()+lname.lower()+"/pub.htm"
       else:
          fnamefinal = fnamef
          lnamef = lname
          url="http://www.library.utoronto.ca/canpoetry/"+lname.lower()+"/pub.htm"
    else:
       fnamefinal = fnamef
       lnamef = lname
       url="http://www.library.utoronto.ca/canpoetry/"+lname.lower()+"/pub.htm"

    #print url, lnamef, fname
    page=urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    
    #page = open("http://www.library.utoronto.ca/canpoetry/page/pub.htm", 'r')
    #soup = BeautifulSoup(page)
    tagS=soup.findAll('li')
    #print tagS, type(tagS), type(tagS[0])
    #print "hello"
    myTagSearch = str(soup.findAll('li'))
    
    #Splits string generated, for some reason BS does not return a list in the previous step
    #It should, but it doesn't
    lista = myTagSearch.split("</li>")
    #last item is not necessary
    lista.pop()
    
    #creates a new file named after the last name of the author
    #uses variable defined previously
    risfilename=lname+".ris"
    #myFile = open(risfilename, 'w+')
    
    #variable to set the item type
    itemtype="BOOK"
    ty="TY  - "+itemtype+"\n"
    #myFile.write("Hello!")
    #Call the function to create the author's list of publications
    risfilename=lname+".ris"
    myFile = open(risfilename, 'w+')
    #print lnamef, fnamefinal
    CreateAuthPubsBooks(lista, ty, lnamef, fnamefinal, myFile, tagS)
    

#These find the info to fill the info tags in the RIS file

#0BIBLIOGRAPHIC TERMS CLASS

class TermFinder:
    def __init__(self, itemclass):
        self.bibitem=itemclass
        self.splitpub=[]
        self.splitbyspace=[]
        self.splitbcolon=[]
    def __str__(self):
        return str(self)
#Title Finder
    def yearfinder(self):
        self.splitter()
        
        for word in self.splitpub:
            #print word
            if len(word)>2:
                if (word[0]=='1' and word[1]=='9') or (word[0]=='2' and word[1]=='0') and len(word)>3:
                    return word[0:4]

    def splitter(self):
        #print self.bibitem.contents[0], type(self.bibitem.contents[0])
        #print self.bibitem, type(self.bibitem)
        #print self.bibitem, type(self.bibitem)
        newstring = str(self.bibitem) # type(self.bibitem.contents[1])
        newst2 = newstring.replace("(","").replace(")","")
        #print newst2
        #newstring = self.bibitem.findAll().contents[0]
        #print newstring, type(newstring)
        splitted = newst2.split("</i>")
        #Split by spaces to find the year element
        self.splitbyspace = newst2.split(" ")
        #Eliminate title element by finding the words in italics
        num=0
        #print splitted
        for i in splitted: 
            #print i
            num+=1
            notitle=[]
            notitle=splitted
            if "<i>" in i:
                notitle.pop(num-1)
        #print type(notitle)
        #print notitle
        noli = notitle[0].replace(".</li>","")
        listitems=[]
        colonsplit=[]
        commasplit=noli.split(", ")
        for i in commasplit:
            listitems.append(i.split(". "))
            self.splitbcolon=listitems
            #print listitems
            for q in listitems:
                #print q, type(q)
                if type(q) is str:
                   colonsplit.append(q.split(": "))
                elif type(q) is list:
                   for r in q:
                       colonsplit.append(r.split(": "))
        new = []
        for p in colonsplit:
            #print colonsplit, p, type(p)
            new = new + p
        #p.replace(".","").replace(",","").replace(":","")
        #print new
        new2 = []  
        new2 = list(set(new))

        #print new2
        self.splitpub=new2
        return splitted
    
def ISBNFinder(self):
        ISBN = ""
        num = 0
        #print self.splitpub
        splitspace = []
        splitskip2 = []
        splitskip = self.bibitem.encode('utf-8').strip().split("/n")
        for i in splitskip:
            splitskip2.append(i.split("\n"))
        for j in splitskip2:
            splitspace.append(i.split(" "))
        
        #print splitspace
        num2=0
        for i in splitspace[0]:
            if type(i) is list:
               for x in i:
                   print x
                   num2+1
                   if "ISBN" in i:
                      ISBN = splitspace[num2]
            else:
                #print i
                num2+1
                if "ISBN" in i:
                   ISBN = splitspace[num2]
        num3=0
        if type(ISBN) is list:
           for t in ISBN:
               print t
               num3+=1
               if "ISBN" in t:
                  print ISBN
                  ISBN = ISBN[num3]
        #print ISBN, type(ISBN)
        #print "Hello world"

        
        for i in self.splitpub:
            num+=1
            i.replace("</li>","")
            #print i
            if is_number(i) and len(i)>5:
               
               ISBN=i
 
            if "ISBN" in i:
               
               complete = i.encode('utf-8').strip()
               splitted = complete.split(" ")
               if len(splitted)==1 and ISBN == "":
                  ISBN = self.splitpub[num]
               elif ISBN == "":
                  ISBN = splitted[1]
        ISBN.replace("\n", "").replace("\r","").replace("</li>","").replace(".","").replace(",","") 
        #print ISBN
        return ISBN

    
    def cityfinder(self):
        global cities
        for i in cities:
            if i in str(self.bibitem):
               return i 

    def pubFinder(self):
        global bookpublishers
        self.splitter()
        for item in self.splitpub:
            for i in bookpublishers:
                if i == item:
                   return i
            #print self.bibitem
            #if self.bibitem in
    def titleFinder(self):
        start = ""
        if "<i>" in str(self.bibitem):
           start = self.bibitem.find("i").contents[0]
        elif "<em>" in str(self.bibitem):
           start = self.bibitem.find("em").contents[0]
        #print str(start), type(start)
        return str(start)
#Searches items with child word and returns a children's book keyword if found
    def childKWfinder(self):
        if "child" in self.bibitem:
           kw="Children's Book"
           return kw
#END OF HELPER FUNCTIONS
#END OF TERM FINDER CLASS




def CreateAuthPubsBooks(lista, ty, lnauthor, fnauthor, myFile, tagS):
#loop to go through every bibliography item found by BeautifulSoup
    #print fnauthor, lnauthor

    #print tagS, len(tagS)
    for item in tagS:
        print item
        #Class instantiation
        #b stands for Book
        b = TermFinder(item)
    #TITLE FINDER
        myFile.write(ty)
       # print lista[-1]
        title = b.titleFinder()
        titlee = title.encode('ascii','ignore')
        myFile.write(str("T1  - "+titlee+"\n"))
        #L1= RIS tag for ISBN
        
        myFile.write(str("A1  - "+lnauthor+", "+fnauthor+"\n")) 
        #KEYWORDS
        #child
        if type(b.childKWfinder()) is str:
           myFile.write(str("KW  - "+b.childKWfinder()+"\n"))
        #CITY
        city=b.cityfinder()
        #Get Publisher
        publisher=b.pubFinder()
        if type(publisher) is str:
           myFile.write(str("PB  - "+publisher+"\n"))
        #Get ISBN
        ISBN = b.ISBNFinder()
        #if type(ISBN) is str:
           #myFile.write(str("L1  - "+ISBN+"\n"))
        #print city, type(city)
        if type(city) is str:
           myFile.write("CY  - "+city+"\n")
        #YEAR FINDER
        year=b.yearfinder()
        if type(year) is str:
           myFile.write("PY  - "+year+"\n")
        #print lisplitter(item)
    
        #ending tag
        myFile.write("RE  -\n")
  
for i in canpoetryAuthors:
    author = []
    #print i, type(i)
    fname= i
    lname=canpoetryAuthors[i]
    #print lname, type(lname)
    #print fname, type(fname)
    if type(fname) is tuple:
       fnamef = str(fname[0])+" "+str(fname[1])
    else:
       fnamef = fname
    GetAuthorList(lname,fnamef)
