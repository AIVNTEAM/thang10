import fresh_tomatoes
import media

toy_story = media.Movie("Toy Story",
                        "A story of the boy and his toys that come to a life",
                        "http://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
                        "https://www.youtube.com/watch?v=r43jY5U7szA")

#print(toy_story.title,toy_story.storyline,toy_story.image,toy_story.trailer)
avartar = media.Movie("Avatar title", "Avatar story", "Avartar Image","https://www.youtube.com/watch?v=r43jY5U7szA")

#print(avartar.title)

school_of_rock = media.Movie("school_of_rock", "Avatar story", "http://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg","https://www.youtube.com/watch?v=czwIjmLLugQ")

ratatouille = media.Movie("ratatouille", "Avatar story", "http://upload.wikimedia.org/wikipedia/en/5/50/RatatouillePoster.jpg","https://www.youtube.com/watch?v=KSVKF0o2kfg")

hunger_games = media.Movie("hunger_games", "Avatar story", "https://www.wikidata.org/wiki/Wikidata:Introduction#/media/File:Datamodel_in_Wikidata.svg","https://www.youtube.com/watch?v=kabFiWsEiS4")

midnight_in_paris = media.Movie("midnight_in_paris", "Avatar story", "http://upload.wikimedia.org/wikipedia/en/5/50/RatatouillePoster.jpg","https://www.youtube.com/watch?v=r43jY5U7szA")

#avartar.show_trailer()

movies =[toy_story,avartar,school_of_rock,ratatouille,hunger_games,midnight_in_paris]
fresh_tomatoes.open_movies_page(movies)
