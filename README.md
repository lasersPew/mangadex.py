# mangadex
A python wrapper for the mangadex API V5. It uses the requests library and all the aditional arguments can ve viewed in the [Official Mangadex Documentation](https://api.mangadex.org/docs.html)

# Instaling the API
## PyPI

```
pip install mangadex
```

## Installing via setuptools
```
python setup.py install --user
```

# Using the API
```py
>>> import mangadex
>>> api = mangadex.Api()
```

# Public Calls

## Getting the latest manga
This is called mangalist in the [documentation](https://api.mangadex.org/docs.html#operation/get-search-manga)
```py
>>> manga_list = api.get_manga_list(limit = 1) #limits the query to return just one manga
>>> manga_list
Manga(id = 0001183c-2089-48e9-96b7-d48db5f1a611, title = {'en': 'Eight'}, altTitles = [{'en': '8 -Eight-'}, {'en': '８－エイト－'}, {'en': 'Eight'}, {'en': 'Eito'}, 
{'en': 'エイト'}], 
description = {'en': 'Tokyo in the 90s, the city center has been suffering from a continuing depopulation. Also affected is the Udagawa Junior High School where only six people are left, as their class leader, protector and very good friend Masato just died in an illegal skateboarding race. Five months later Eito Hachiya, nickname: Eight or &quot;8&quot; enrolls in school and wants to find out what happened. He even just looks like Masato! But mysteries surround him: Why does he know all the other six? Why can&rsquo;t they remember him?\r\n\r\nNote: Was cancelled after ~25% of volume 4, the epilogue consists of an alternative ending for Eight.'}, 
isLocked = False, links = {'al': '38734', 'ap': 'eight', 'kt': '17709', 'mu': '6521', 'mal': '8734'}, originalLanguage = ja 
lastVolume = None, lastChapter = 37.6, publicationDemographic = seinen, status = completed, year = None, contentRating = safe 
```
You can algo use the `get_manga_list()` method to search for manga. 

The usage is like this
```py
>>> manga_list = api.get_manga_list(title = "You manga title here")
```

**NOTE**: The search rigth now is faulty but tahts is an api problem. At the moment the only parameters that work are: `title`, `limit` and `offset`

## Getting a manga by its id
```py
>>> manga = api.view_manga_by_id(id = "0001183c-2089-48e9-96b7-d48db5f1a611")
```

## Random manga

```py
>>> random_manga = api.random_manga()
```

## Manga Feed

Get the chapter, or chapters from the feed of a specific manga.

```py
>>> manga_feed = api.manga_feed(id = "0001183c-2089-48e9-96b7-d48db5f1a611", limit = 1)
[Chapter(id = 015979c8-ffa4-4afa-b48e-3da6d10279b0, title = Navel-Gazing, volume = 3, chapter = 23, translatedLanguage = en, hash = bf986ab3bc4471980430b7c5ec407ee0 
 data = ['x1-fcec4beb464a2071023a92ec1192a3b7e3b7c5ae531fa8cc8a7d874056f509a0.jpg', 'x2-4b3bdefecd786fc64823eb118fb52da5646f44827fa82379b9b710bfe368ecbe.jpg',
  'x3-7f0fbee875edaaa511f58fdd4c75092e86a88c57722b84bda36adffbda485b9f.jpg', 'x4-933b914b685fcef4b241e91e265293ef520efa34e9da2a8a52344eab360ca6ce.jpg', 
  'x5-905e50681548041b288d7a985ba5c3415e441ef7e7d87da786edd3206d1f02ef.jpg'], publishAt = 2018-03-19 01:32:00+00:00, createdAt = 2018-03-19 01:32:00+00:00, uploadedAt = 
  2018-03-19 01:32:00+00:00, sacanlation_group_id = 59957a04-fa91-4099-921d-7e7988a19acb, Mangaid = 0001183c-2089-48e9-96b7-d48db5f1a611, uploader = 
  e19519ce-8c5f-4d7c-8280-704a87d34429)]
```
## Get manga volumnes and chapters
Get a manga volumes and chapters

```py
>>> api.get_manga_volumes_and_chapters(id = "the manga id")
```

## Get Chapter

Returns a Chpater Object  by its id

```py
>>> chapter = api.get_chapter(id = "015979c8-ffa4-4afa-b48e-3da6d10279b0")
>> chapter
Chapter(id = 015979c8-ffa4-4afa-b48e-3da6d10279b0, title = Navel-Gazing, volume = 3, chapter = 23, translatedLanguage = en, hash = bf986ab3bc4471980430b7c5ec407ee0 
data = ['x1-fcec4beb464a2071023a92ec1192a3b7e3b7c5ae531fa8cc8a7d874056f509a0.jpg', 'x2-4b3bdefecd786fc64823eb118fb52da5646f44827fa82379b9b710bfe368ecbe.jpg', 'x3-7f0fbee875edaaa511f58fdd4c75092e86a88c57722b84bda36adffbda485b9f.jpg', 'x4-933b914b685fcef4b241e91e265293ef520efa34e9da2a8a52344eab360ca6ce.jpg', 'x5-905e50681548041b288d7a985ba5c3415e441ef7e7d87da786edd3206d1f02ef.jpg'], publishAt = 2018-03-19 01:32:00+00:00, createdAt = 2018-03-19 01:32:00+00:00, uploadedAt = 2018-03-19 01:32:00+00:00, sacanlation_group_id = 59957a04-fa91-4099-921d-7e7988a19acb, Mangaid = 0001183c-2089-48e9-96b7-d48db5f1a611, uploader = e19519ce-8c5f-4d7c-8280-704a87d34429)
```

## Chapter List
It will return a list of chapters

```py
>>> chapter_list = api.chapter_list()
```
If you want the chpaters of a given Manga, you'll need to specify the [feed endpoints](https://api.mangadex.org/docs.html#operation/get-search-group)

## Chapter Images

Return the links for the chapter images fot a given Chapter Object
```py
>>> chapter_images = api.fetch_chapter_images(Chapter)
```

## Get User

Get a User by id
```py
>>> user = api.get_user(id = "id of user")
```


## Tag List

The list of the manga tags

```py
>>> tag_list = api.tag_list()
```

## Get scanlation group list

Get a Scanlation Group list

```py
>>> api.scanlation_group_list()
```


# Private Calls

## Login

Method to login to the website
```py
>>> api.login(username = USERNAME, password = PASSWORD)
```
It is recomended that you add this values to you path for security reasons.

## Your User Info
Get your user info

```py
>>> my_user = api.me()
```

## Get Logged User Followed Manga List

Get your manga follow list!

```py
>>> follow_list = api.get_my_mangalist()
```
This functions, as well as most of the other ones accept optional parameters.
This are:
* `limit` : limits the amout of results. It accepts a value between 1 and 100, the default if 10
* `offset` : Makes an offset of the velue provided to the list. Accepts values >= 0

## Get Logged User Followed Groups

Get the list of the Scanlination group you follow!

```py
>>> scangroups_followlist = api.get_my_followed_groups()
```

## Get Logged User Followed Users

The list of the users you follow

```py
>>> followed_users = api.get_my_followed_users()
```

## Get chapters marked as read from a manga

Get a list of the capters marked as read for a given manga

```py
>>> read_chapters = api.get_manga_read_markes(id = "the manga id")
```

##  Get all followed manga reading status

Get a list of the all the manga reading stauts

```py
>>> my_manga_reading_stauts = api.get_all_manga_reading_status()
```

## Get a specific manga reading status

Get the reading status of a specific manga

```py
>>> manga_reading_status = api.get_manga_reading_status(id = "the manga id")
```
## Update Manga reading status

```py
>>> api.update_manga_reading_status(id = "the manga id", status = "the new reading status")
```
The `status` parameter can take the following values:
`"reading"` `"on_hold"` `"plan_to_read"` `"dropped"` `"re_reading"` `"completed"` 
## Follow a manga

Follow a manga
```py
>>> api.follow_manga(id = "the manga id")
```

## Unfollow a manga
Unfollows a manga
```py
>>>api.unfollow_manga(id = "the manga id")
```

## Create manga
Creates a manga
```py
>>> api.create_manga(title = "manga title", )
```
## Update Manga
Updates a manga

```py
>>> api.update_manga(id = "the manga id")
```

## Delete Manga
Deletes manga

```py
>>> api.delete_manga(id = "the manga id")
```
## Add manga to custom list

Add a manga to a custom list

```py
>>> api.add_manga_to_custom_list(id = "the manga id", listId = "the list id")
```

## Remove a manga from custom list

Removes a manga from a custom list

```py
>>> api.remove_manga_from_custom_list(id = "the manga id", listId = "the list id")
```

## Create  a custom list

```py
>>> api.create_customlist() #this will create a custom list with no special parameters
```
### Query parameters:
* `name`. The custom list name
* `visibility`. The visibility of the custom list. Default public
* `manga`. The list of manga ids

## Get custom list
```py
>>> api.get_customlist(id = "th custom list id")
```

## Update custom list
```py
>>> api.update_customlist(id = "the custom list id")
```

### Query parameters:
* `name`. The custom list name
* `visibility`. Values : `"public"` `"private"`

## Delete custom list

```py
>>> api.delete_customlist(id = "the custom list id")
```

## Get User Custom list
```py
>>> api.get_user_customlists(id = "the user id")
```

### QueryParams:

* `limit`. The limit of custom lists to return
* `offset`. The amout of offset

## Get custom list manga feed:
```py
>>> api.get_customlist_manga_feed(id = "the custom list id")
```
### QueryParams:

* limit
* offset
* locales
* createdAtSince. Datetime String with the following format YYYY-MM-DDTHH:MM:SS
* updatedAtSince. Datetime String with the following format YYYY-MM-DDTHH:MM:SS
* publishAtSince. Datetime String with the following format YYYY-MM-DDTHH:MM:SS

## Create Author

```py
>>> api.create_author(name = "author name", version = 1, ObjReturn = False)
```
## Update Author

```py
>>> api.update_author(id = "the author id", version = "int with the version", name = "author's name", ObjReturn = False)
```

## Delete Author

```py
>>> api.delete_author(id = "the author id")
```