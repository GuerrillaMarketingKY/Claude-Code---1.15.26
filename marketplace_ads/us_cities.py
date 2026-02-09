"""
Comprehensive list of US cities organized by state.
Covers all 50 states + DC with major cities and metro areas.
"""

US_CITIES = {
    "Alabama": [
        "Birmingham", "Montgomery", "Huntsville", "Mobile", "Tuscaloosa",
        "Hoover", "Dothan", "Auburn", "Decatur", "Madison",
        "Florence", "Gadsden", "Vestavia Hills", "Prattville", "Phenix City",
        "Alabaster", "Opelika", "Enterprise", "Homewood", "Northport",
        "Anniston", "Prichard", "Athens", "Daphne", "Pelham",
        "Oxford", "Albertville", "Selma", "Troy", "Helena"
    ],
    "Alaska": [
        "Anchorage", "Fairbanks", "Juneau", "Wasilla", "Sitka",
        "Ketchikan", "Kenai", "Kodiak", "Bethel", "Palmer",
        "Homer", "Soldotna", "Valdez", "Nome", "Barrow",
        "Seward", "Cordova", "Petersburg", "Wrangell", "Kotzebue"
    ],
    "Arizona": [
        "Phoenix", "Tucson", "Mesa", "Chandler", "Scottsdale",
        "Glendale", "Gilbert", "Tempe", "Peoria", "Surprise",
        "Yuma", "Avondale", "Goodyear", "Flagstaff", "Buckeye",
        "Lake Havasu City", "Casa Grande", "Maricopa", "Sierra Vista", "Prescott",
        "Bullhead City", "Apache Junction", "Prescott Valley", "Marana", "El Mirage",
        "Kingman", "Queen Creek", "Florence", "San Luis", "Sahuarita"
    ],
    "Arkansas": [
        "Little Rock", "Fort Smith", "Fayetteville", "Springdale", "Jonesboro",
        "North Little Rock", "Conway", "Rogers", "Pine Bluff", "Bentonville",
        "Hot Springs", "Benton", "Texarkana", "Sherwood", "Jacksonville",
        "Russellville", "Bella Vista", "West Memphis", "Paragould", "Cabot",
        "Searcy", "Van Buren", "Bryant", "Maumelle", "Centerton"
    ],
    "California": [
        "Los Angeles", "San Diego", "San Jose", "San Francisco", "Fresno",
        "Sacramento", "Long Beach", "Oakland", "Bakersfield", "Anaheim",
        "Santa Ana", "Riverside", "Stockton", "Irvine", "Chula Vista",
        "Fremont", "San Bernardino", "Modesto", "Moreno Valley", "Fontana",
        "Glendale", "Huntington Beach", "Santa Clarita", "Garden Grove", "Oceanside",
        "Rancho Cucamonga", "Ontario", "Santa Rosa", "Elk Grove", "Corona",
        "Lancaster", "Palmdale", "Salinas", "Pomona", "Hayward",
        "Escondido", "Sunnyvale", "Torrance", "Pasadena", "Orange",
        "Fullerton", "Thousand Oaks", "Roseville", "Concord", "Simi Valley",
        "Santa Clara", "Victorville", "Vallejo", "Berkeley", "El Monte",
        "Downey", "Costa Mesa", "Inglewood", "Carlsbad", "Fairfield",
        "Murrieta", "Temecula", "West Covina", "Norwalk", "Richmond",
        "Burbank", "Antioch", "Daly City", "El Cajon", "San Mateo",
        "Rialto", "Clovis", "Compton", "Jurupa Valley", "Vista",
        "South Gate", "Mission Viejo", "Vacaville", "Carson", "Hesperia",
        "Redding", "Santa Maria", "Westminster", "Santa Barbara", "Chico",
        "Newport Beach", "San Leandro", "San Marcos", "Whittier", "Hawthorne",
        "Citrus Heights", "Alhambra", "Tracy", "Livermore", "Buena Park",
        "Menifee", "Hemet", "Lakewood", "Merced", "Chino",
        "Indio", "Redwood City", "Lake Forest", "Napa", "Tustin"
    ],
    "Colorado": [
        "Denver", "Colorado Springs", "Aurora", "Fort Collins", "Lakewood",
        "Thornton", "Arvada", "Westminster", "Pueblo", "Centennial",
        "Boulder", "Greeley", "Longmont", "Loveland", "Broomfield",
        "Castle Rock", "Commerce City", "Parker", "Littleton", "Northglenn",
        "Brighton", "Englewood", "Wheat Ridge", "Fountain", "Lafayette",
        "Windsor", "Erie", "Evans", "Golden", "Louisville"
    ],
    "Connecticut": [
        "Bridgeport", "New Haven", "Stamford", "Hartford", "Waterbury",
        "Norwalk", "Danbury", "New Britain", "Bristol", "Meriden",
        "Milford", "West Haven", "Middletown", "Norwich", "Shelton",
        "Torrington", "New London", "Ansonia", "Derby", "Groton",
        "Windham", "Naugatuck", "Glastonbury", "Newington", "Cheshire"
    ],
    "Delaware": [
        "Wilmington", "Dover", "Newark", "Middletown", "Bear",
        "Glasgow", "Brookside", "Hockessin", "Smyrna", "Milford",
        "Seaford", "Georgetown", "Elsmere", "New Castle", "Millsboro"
    ],
    "Florida": [
        "Jacksonville", "Miami", "Tampa", "Orlando", "St. Petersburg",
        "Hialeah", "Tallahassee", "Fort Lauderdale", "Port St. Lucie", "Cape Coral",
        "Pembroke Pines", "Hollywood", "Miramar", "Gainesville", "Coral Springs",
        "Miami Gardens", "Clearwater", "Palm Bay", "Pompano Beach", "West Palm Beach",
        "Lakeland", "Davie", "Miami Beach", "Sunrise", "Boca Raton",
        "Deltona", "Plantation", "Large", "Deerfield Beach", "Palm Coast",
        "Melbourne", "Boynton Beach", "Lauderhill", "Weston", "Kissimmee",
        "Homestead", "Tamarac", "Delray Beach", "Daytona Beach", "North Miami",
        "Wellington", "North Port", "Jupiter", "Coconut Creek", "Port Orange",
        "Sanford", "Margate", "Ocala", "Sarasota", "Pensacola",
        "Bradenton", "Panama City", "Fort Myers", "Naples", "Key West",
        "Destin", "Winter Haven", "Apopka", "Ocoee", "Clermont"
    ],
    "Georgia": [
        "Atlanta", "Augusta", "Columbus", "Macon", "Savannah",
        "Athens", "Sandy Springs", "Roswell", "Johns Creek", "Albany",
        "Warner Robins", "Alpharetta", "Marietta", "Valdosta", "Smyrna",
        "Dunwoody", "Brookhaven", "Peachtree City", "Newnan", "Dalton",
        "Gainesville", "Milton", "Hinesville", "Douglasville", "Kennesaw",
        "Statesboro", "Lawrenceville", "Duluth", "Stockbridge", "Woodstock"
    ],
    "Hawaii": [
        "Honolulu", "Pearl City", "Hilo", "Kailua", "Waipahu",
        "Kaneohe", "Mililani Town", "Kahului", "Ewa Gentry", "Mililani Mauka",
        "Kihei", "Makakilo", "Wahiawa", "Schofield Barracks", "Kapolei",
        "Wailuku", "Aiea", "Kailua-Kona", "Lahaina", "Waimalu"
    ],
    "Idaho": [
        "Boise", "Meridian", "Nampa", "Idaho Falls", "Caldwell",
        "Pocatello", "Coeur d'Alene", "Twin Falls", "Lewiston", "Post Falls",
        "Rexburg", "Eagle", "Moscow", "Kuna", "Ammon",
        "Chubbuck", "Mountain Home", "Garden City", "Blackfoot", "Burley"
    ],
    "Illinois": [
        "Chicago", "Aurora", "Rockford", "Joliet", "Naperville",
        "Springfield", "Peoria", "Elgin", "Waukegan", "Champaign",
        "Bloomington", "Decatur", "Evanston", "Des Plaines", "Berwyn",
        "Wheaton", "Belleville", "Elmhurst", "DeKalb", "Moline",
        "Urbana", "Crystal Lake", "Quincy", "Rock Island", "Park Ridge",
        "Calumet City", "Glenview", "Normal", "Hoffman Estates", "Skokie",
        "Arlington Heights", "Bolingbrook", "Palatine", "Schaumburg", "Oak Lawn",
        "Tinley Park", "Orland Park", "Downers Grove", "Oak Park", "Buffalo Grove"
    ],
    "Indiana": [
        "Indianapolis", "Fort Wayne", "Evansville", "South Bend", "Carmel",
        "Fishers", "Bloomington", "Hammond", "Gary", "Lafayette",
        "Muncie", "Terre Haute", "Kokomo", "Noblesville", "Anderson",
        "Greenwood", "Elkhart", "Mishawaka", "Lawrence", "Jeffersonville",
        "Columbus", "Portage", "New Albany", "Richmond", "Westfield",
        "Valparaiso", "Goshen", "Michigan City", "West Lafayette", "Marion"
    ],
    "Iowa": [
        "Des Moines", "Cedar Rapids", "Davenport", "Sioux City", "Iowa City",
        "Waterloo", "Council Bluffs", "Ames", "West Des Moines", "Dubuque",
        "Ankeny", "Urbandale", "Cedar Falls", "Marion", "Bettendorf",
        "Mason City", "Marshalltown", "Clinton", "Burlington", "Ottumwa",
        "Fort Dodge", "Muscatine", "Coralville", "Johnston", "North Liberty"
    ],
    "Kansas": [
        "Wichita", "Overland Park", "Kansas City", "Olathe", "Topeka",
        "Lawrence", "Shawnee", "Manhattan", "Lenexa", "Salina",
        "Hutchinson", "Leavenworth", "Leawood", "Dodge City", "Garden City",
        "Emporia", "Derby", "Prairie Village", "Junction City", "Hays",
        "Liberal", "Newton", "Pittsburg", "Great Bend", "McPherson"
    ],
    "Kentucky": [
        "Louisville", "Lexington", "Bowling Green", "Owensboro", "Covington",
        "Richmond", "Georgetown", "Florence", "Hopkinsville", "Nicholasville",
        "Elizabethtown", "Henderson", "Frankfort", "Paducah", "Ashland",
        "Radcliff", "Murray", "Erlanger", "Winchester", "St. Matthews",
        "Danville", "Burlington", "Fort Thomas", "Madisonville", "Shelbyville"
    ],
    "Louisiana": [
        "New Orleans", "Baton Rouge", "Shreveport", "Metairie", "Lafayette",
        "Lake Charles", "Kenner", "Bossier City", "Monroe", "Alexandria",
        "Houma", "Marrero", "New Iberia", "Laplace", "Slidell",
        "Prairieville", "Central", "Ruston", "Sulphur", "Hammond",
        "Harvey", "Bayou Cane", "Natchitoches", "Opelousas", "Zachary"
    ],
    "Maine": [
        "Portland", "Lewiston", "Bangor", "South Portland", "Auburn",
        "Biddeford", "Sanford", "Augusta", "Saco", "Westbrook",
        "Waterville", "Presque Isle", "Brewer", "Bath", "Caribou",
        "Ellsworth", "Old Town", "Rockland", "Belfast", "Gardiner"
    ],
    "Maryland": [
        "Baltimore", "Columbia", "Germantown", "Silver Spring", "Waldorf",
        "Glen Burnie", "Ellicott City", "Frederick", "Dundalk", "Rockville",
        "Bethesda", "Gaithersburg", "Towson", "Bowie", "Aspen Hill",
        "Wheaton", "Bel Air", "College Park", "Annapolis", "Hagerstown",
        "Severn", "Odenton", "Clinton", "Catonsville", "Salisbury",
        "Laurel", "Severna Park", "Crofton", "Cumberland", "Owings Mills"
    ],
    "Massachusetts": [
        "Boston", "Worcester", "Springfield", "Cambridge", "Lowell",
        "Brockton", "New Bedford", "Quincy", "Lynn", "Fall River",
        "Newton", "Lawrence", "Somerville", "Framingham", "Haverhill",
        "Waltham", "Malden", "Medford", "Taunton", "Chicopee",
        "Weymouth", "Revere", "Peabody", "Methuen", "Barnstable",
        "Pittsfield", "Attleboro", "Everett", "Salem", "Westfield"
    ],
    "Michigan": [
        "Detroit", "Grand Rapids", "Warren", "Sterling Heights", "Ann Arbor",
        "Lansing", "Flint", "Dearborn", "Livonia", "Troy",
        "Westland", "Farmington Hills", "Kalamazoo", "Wyoming", "Southfield",
        "Rochester Hills", "Taylor", "Pontiac", "St. Clair Shores", "Royal Oak",
        "Novi", "Dearborn Heights", "Battle Creek", "Saginaw", "Kentwood",
        "East Lansing", "Roseville", "Portage", "Midland", "Lincoln Park",
        "Muskegon", "Holland", "Bay City", "Jackson", "Traverse City"
    ],
    "Minnesota": [
        "Minneapolis", "St. Paul", "Rochester", "Bloomington", "Duluth",
        "Brooklyn Park", "Plymouth", "Maple Grove", "Woodbury", "St. Cloud",
        "Eagan", "Eden Prairie", "Blaine", "Lakeville", "Minnetonka",
        "Burnsville", "Apple Valley", "Edina", "St. Louis Park", "Mankato",
        "Moorhead", "Shakopee", "Maplewood", "Cottage Grove", "Richfield",
        "Roseville", "Inver Grove Heights", "Andover", "Coon Rapids", "Savage"
    ],
    "Mississippi": [
        "Jackson", "Gulfport", "Southaven", "Hattiesburg", "Biloxi",
        "Meridian", "Tupelo", "Olive Branch", "Greenville", "Horn Lake",
        "Clinton", "Pearl", "Madison", "Starkville", "Columbus",
        "Vicksburg", "Pascagoula", "Oxford", "Laurel", "Brandon",
        "Ridgeland", "Corinth", "Hernando", "Natchez", "Clarksdale"
    ],
    "Missouri": [
        "Kansas City", "St. Louis", "Springfield", "Columbia", "Independence",
        "Lee's Summit", "O'Fallon", "St. Joseph", "St. Charles", "St. Peters",
        "Blue Springs", "Florissant", "Joplin", "Chesterfield", "Jefferson City",
        "Cape Girardeau", "Wildwood", "University City", "Ballwin", "Raytown",
        "Liberty", "Wentzville", "Kirkwood", "Maryland Heights", "Hazelwood",
        "Gladstone", "Grandview", "Belton", "Webster Groves", "Sedalia"
    ],
    "Montana": [
        "Billings", "Missoula", "Great Falls", "Bozeman", "Butte",
        "Helena", "Kalispell", "Havre", "Anaconda", "Miles City",
        "Belgrade", "Livingston", "Laurel", "Whitefish", "Lewistown",
        "Sidney", "Glendive", "Glasgow", "Dillon", "Hamilton"
    ],
    "Nebraska": [
        "Omaha", "Lincoln", "Bellevue", "Grand Island", "Kearney",
        "Fremont", "Hastings", "Norfolk", "North Platte", "Columbus",
        "Papillion", "La Vista", "Scottsbluff", "South Sioux City", "Beatrice",
        "Lexington", "Chalco", "Gering", "Alliance", "Blair"
    ],
    "Nevada": [
        "Las Vegas", "Henderson", "Reno", "North Las Vegas", "Sparks",
        "Carson City", "Fernley", "Elko", "Mesquite", "Boulder City",
        "Fallon", "Winnemucca", "West Wendover", "Ely", "Yerington",
        "Pahrump", "Spring Creek", "Gardnerville Ranchos", "Dayton", "Sun Valley"
    ],
    "New Hampshire": [
        "Manchester", "Nashua", "Concord", "Derry", "Dover",
        "Rochester", "Salem", "Merrimack", "Hudson", "Londonderry",
        "Keene", "Bedford", "Portsmouth", "Goffstown", "Laconia",
        "Hampton", "Milford", "Durham", "Exeter", "Windham"
    ],
    "New Jersey": [
        "Newark", "Jersey City", "Paterson", "Elizabeth", "Lakewood",
        "Edison", "Woodbridge", "Toms River", "Hamilton", "Trenton",
        "Clifton", "Camden", "Brick", "Cherry Hill", "Passaic",
        "Middletown", "Union City", "Old Bridge", "Gloucester Township", "North Bergen",
        "Vineland", "Bayonne", "East Orange", "Franklin", "Piscataway",
        "New Brunswick", "West New York", "Perth Amboy", "Plainfield", "Hackensack",
        "Sayreville", "Hoboken", "Kearny", "Linden", "Atlantic City"
    ],
    "New Mexico": [
        "Albuquerque", "Las Cruces", "Rio Rancho", "Santa Fe", "Roswell",
        "Farmington", "South Valley", "Clovis", "Hobbs", "Alamogordo",
        "Carlsbad", "Gallup", "Deming", "Los Lunas", "Chaparral",
        "Sunland Park", "Las Vegas", "Portales", "Los Alamos", "Artesia"
    ],
    "New York": [
        "New York City", "Buffalo", "Rochester", "Yonkers", "Syracuse",
        "Albany", "New Rochelle", "Mount Vernon", "Schenectady", "Utica",
        "White Plains", "Hempstead", "Troy", "Niagara Falls", "Binghamton",
        "Freeport", "Valley Stream", "Long Beach", "Spring Valley", "Rome",
        "Ithaca", "Poughkeepsie", "North Tonawanda", "Jamestown", "Elmira",
        "Saratoga Springs", "Middletown", "Watertown", "Auburn", "Newburgh",
        "Lindenhurst", "Massapequa Park", "Oswego", "Plattsburgh", "Glens Falls"
    ],
    "North Carolina": [
        "Charlotte", "Raleigh", "Greensboro", "Durham", "Winston-Salem",
        "Fayetteville", "Cary", "Wilmington", "High Point", "Concord",
        "Greenville", "Asheville", "Gastonia", "Jacksonville", "Chapel Hill",
        "Huntersville", "Apex", "Burlington", "Kannapolis", "Rocky Mount",
        "Mooresville", "Holly Springs", "Wake Forest", "Indian Trail", "Cornelius",
        "Sanford", "Hickory", "Matthews", "Monroe", "Salisbury",
        "New Bern", "Goldsboro", "Lumberton", "Thomasville", "Kernersville"
    ],
    "North Dakota": [
        "Fargo", "Bismarck", "Grand Forks", "Minot", "West Fargo",
        "Williston", "Dickinson", "Mandan", "Jamestown", "Wahpeton",
        "Devils Lake", "Watford City", "Valley City", "Grafton", "Beulah",
        "Rugby", "Bottineau", "Carrington", "Lisbon", "Harvey"
    ],
    "Ohio": [
        "Columbus", "Cleveland", "Cincinnati", "Toledo", "Akron",
        "Dayton", "Parma", "Canton", "Youngstown", "Lorain",
        "Hamilton", "Springfield", "Kettering", "Elyria", "Lakewood",
        "Cuyahoga Falls", "Euclid", "Middletown", "Mansfield", "Newark",
        "Mentor", "Beavercreek", "Cleveland Heights", "Strongsville", "Dublin",
        "Fairfield", "Findlay", "Warren", "Lancaster", "Lima",
        "Huber Heights", "Westerville", "Marion", "Grove City", "Mason"
    ],
    "Oklahoma": [
        "Oklahoma City", "Tulsa", "Norman", "Broken Arrow", "Edmond",
        "Lawton", "Moore", "Midwest City", "Enid", "Stillwater",
        "Muskogee", "Bartlesville", "Owasso", "Shawnee", "Yukon",
        "Ardmore", "Ponca City", "Duncan", "Del City", "Bixby",
        "Sapulpa", "Altus", "Bethany", "Sand Springs", "Claremore"
    ],
    "Oregon": [
        "Portland", "Salem", "Eugene", "Gresham", "Hillsboro",
        "Beaverton", "Bend", "Medford", "Springfield", "Corvallis",
        "Albany", "Tigard", "Lake Oswego", "Keizer", "Grants Pass",
        "Oregon City", "McMinnville", "Redmond", "Tualatin", "West Linn",
        "Woodburn", "Forest Grove", "Newberg", "Roseburg", "Ashland",
        "Milwaukie", "Pendleton", "Coos Bay", "The Dalles", "Klamath Falls"
    ],
    "Pennsylvania": [
        "Philadelphia", "Pittsburgh", "Allentown", "Reading", "Erie",
        "Upper Darby", "Scranton", "Bethlehem", "Bensalem", "Lancaster",
        "Harrisburg", "York", "Wilkes-Barre", "Chester", "Abington",
        "Cheltenham", "Lower Merion", "Bristol", "Haverford", "Levittown",
        "State College", "Williamsport", "Easton", "Norristown", "Chambersburg",
        "Pottstown", "Lebanon", "Hazleton", "Johnstown", "West Chester",
        "Carlisle", "Hanover", "Mechanicsburg", "King of Prussia", "Altoona"
    ],
    "Rhode Island": [
        "Providence", "Warwick", "Cranston", "Pawtucket", "East Providence",
        "Woonsocket", "Coventry", "Cumberland", "North Providence", "South Kingstown",
        "West Warwick", "Johnston", "North Kingstown", "Newport", "Bristol",
        "Westerly", "Smithfield", "Lincoln", "Central Falls", "Barrington"
    ],
    "South Carolina": [
        "Charleston", "Columbia", "North Charleston", "Mount Pleasant", "Rock Hill",
        "Greenville", "Summerville", "Goose Creek", "Hilton Head Island", "Florence",
        "Spartanburg", "Myrtle Beach", "Sumter", "Bluffton", "Aiken",
        "Anderson", "Greer", "Mauldin", "Hanahan", "Conway",
        "North Augusta", "Easley", "Simpsonville", "Beaufort", "West Columbia",
        "Clemson", "Lexington", "Irmo", "Fort Mill", "Tega Cay"
    ],
    "South Dakota": [
        "Sioux Falls", "Rapid City", "Aberdeen", "Brookings", "Watertown",
        "Mitchell", "Yankton", "Huron", "Pierre", "Spearfish",
        "Vermillion", "Brandon", "Box Elder", "Madison", "Sturgis",
        "Belle Fourche", "Harrisburg", "Tea", "Dell Rapids", "Mobridge"
    ],
    "Tennessee": [
        "Nashville", "Memphis", "Knoxville", "Chattanooga", "Clarksville",
        "Murfreesboro", "Franklin", "Jackson", "Johnson City", "Bartlett",
        "Hendersonville", "Kingsport", "Collierville", "Smyrna", "Cleveland",
        "Brentwood", "Germantown", "Spring Hill", "Columbia", "La Vergne",
        "Gallatin", "Mount Juliet", "Cookeville", "Lebanon", "Morristown",
        "Oak Ridge", "Maryville", "Bristol", "Farragut", "Shelbyville"
    ],
    "Texas": [
        "Houston", "San Antonio", "Dallas", "Austin", "Fort Worth",
        "El Paso", "Arlington", "Corpus Christi", "Plano", "Laredo",
        "Lubbock", "Garland", "Irving", "Amarillo", "Grand Prairie",
        "Brownsville", "McKinney", "Frisco", "Pasadena", "Mesquite",
        "Killeen", "McAllen", "Midland", "Denton", "Waco",
        "Carrollton", "Round Rock", "Abilene", "Pearland", "Richardson",
        "Odessa", "Sugar Land", "Beaumont", "The Woodlands", "Allen",
        "League City", "San Angelo", "Edinburg", "Conroe", "Bryan",
        "Mission", "Flower Mound", "New Braunfels", "Pharr", "Temple",
        "Tyler", "Missouri City", "North Richland Hills", "Cedar Park", "Leander",
        "Mansfield", "Rowlett", "Georgetown", "Pflugerville", "Wylie",
        "DeSoto", "Burleson", "Port Arthur", "Victoria", "Cedar Hill",
        "Grapevine", "Galveston", "San Marcos", "Harlingen", "Rockwall",
        "Huntsville", "Texarkana", "Sherman", "Lufkin", "Hurst"
    ],
    "Utah": [
        "Salt Lake City", "West Valley City", "Provo", "West Jordan", "Orem",
        "Sandy", "Ogden", "St. George", "Layton", "South Jordan",
        "Lehi", "Millcreek", "Taylorsville", "Logan", "Murray",
        "Draper", "Bountiful", "Riverton", "Roy", "Spanish Fork",
        "Pleasant Grove", "Kearns", "Tooele", "Cottonwood Heights", "Springville",
        "Eagle Mountain", "Herriman", "Clearfield", "Kaysville", "Holladay"
    ],
    "Vermont": [
        "Burlington", "South Burlington", "Rutland", "Barre", "Montpelier",
        "Winooski", "St. Albans", "Newport", "Vergennes", "Brattleboro",
        "Bennington", "Middlebury", "St. Johnsbury", "Morrisville", "Northfield",
        "Lyndonville", "Swanton", "Hartford", "Woodstock", "Springfield"
    ],
    "Virginia": [
        "Virginia Beach", "Norfolk", "Chesapeake", "Richmond", "Newport News",
        "Alexandria", "Hampton", "Roanoke", "Portsmouth", "Suffolk",
        "Lynchburg", "Harrisonburg", "Leesburg", "Charlottesville", "Danville",
        "Manassas", "Petersburg", "Fredericksburg", "Winchester", "Salem",
        "Staunton", "Herndon", "Waynesboro", "Bristol", "Colonial Heights",
        "Radford", "Culpeper", "Vienna", "Ashburn", "Centreville",
        "McLean", "Fairfax", "Dale City", "Lake Ridge", "Woodbridge"
    ],
    "Washington": [
        "Seattle", "Spokane", "Tacoma", "Vancouver", "Bellevue",
        "Kent", "Everett", "Renton", "Spokane Valley", "Federal Way",
        "Yakima", "Bellingham", "Kirkland", "Auburn", "Kennewick",
        "Redmond", "Marysville", "Pasco", "Lakewood", "Sammamish",
        "Richland", "Burien", "Olympia", "Lacey", "Edmonds",
        "Bremerton", "Puyallup", "Lynnwood", "Bothell", "Longview",
        "Issaquah", "Wenatchee", "Mount Vernon", "University Place", "Walla Walla"
    ],
    "West Virginia": [
        "Charleston", "Huntington", "Morgantown", "Parkersburg", "Wheeling",
        "Weirton", "Fairmont", "Martinsburg", "Beckley", "Clarksburg",
        "South Charleston", "St. Albans", "Vienna", "Bluefield", "Elkins",
        "Nitro", "Dunbar", "Princeton", "Bridgeport", "Oak Hill"
    ],
    "Wisconsin": [
        "Milwaukee", "Madison", "Green Bay", "Kenosha", "Racine",
        "Appleton", "Waukesha", "Eau Claire", "Oshkosh", "Janesville",
        "West Allis", "La Crosse", "Sheboygan", "Wauwatosa", "Fond du Lac",
        "New Berlin", "Wausau", "Brookfield", "Beloit", "Greenfield",
        "Franklin", "Oak Creek", "Manitowoc", "West Bend", "Sun Prairie",
        "Superior", "Fitchburg", "Muskego", "Stevens Point", "Menomonee Falls"
    ],
    "Wyoming": [
        "Cheyenne", "Casper", "Laramie", "Gillette", "Rock Springs",
        "Sheridan", "Green River", "Evanston", "Riverton", "Jackson",
        "Cody", "Rawlins", "Lander", "Torrington", "Powell",
        "Douglas", "Worland", "Buffalo", "Wheatland", "Newcastle"
    ],
    "District of Columbia": [
        "Washington"
    ]
}


def get_all_cities():
    """Returns a flat list of (city, state) tuples."""
    cities = []
    for state, city_list in US_CITIES.items():
        for city in city_list:
            cities.append((city, state))
    return cities


def get_total_count():
    """Returns total number of city entries."""
    return sum(len(cities) for cities in US_CITIES.values())
