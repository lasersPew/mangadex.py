from __future__ import absolute_import

import json
import requests

from typing import Tuple, List

try:
    basestring
except NameError:
    from past.builtins import basestring

try:
    from urllib.parse import urlparse, urlencode
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode

from mangadex import (ApiError, ApiClientError, Manga, Tag, Chapter, User, UserError, ChapterError, Author, ScanlationGroup)

class Api():
    def __init__(self, timeout = 5):
        self.URL = 'https://api.mangadex.org'
        self.bearer = None
        self.timeout = timeout

    def _auth_handler(self, json_payload) -> None:
        url = f"{self.URL}/auth/login"
        auth = self._request_url(url, "POST", params = json_payload)
        token = auth['token']['session']
        bearer = {"Authorization" : f"Bearer {token}"}
        self.bearer = bearer

    def _request_url(self, url, method, params = None, headers = None) -> dict:
        if params is None:
            params = {}
        params = {k: v.decode("utf-8") if isinstance(v, bytes) else v for k, v in params.items()}
        
        if method == 'GET':
            url = self._build_url(url, params)
            try:
                resp = requests.get(url, headers=headers, timeout=self.timeout)
            except requests.RequestException as e:
                print(f"An error has occured: {e}")
                raise
        elif method == 'POST':
            try:
                resp = requests.post(url, json = params, headers=headers, timeout=self.timeout)
            except requests.RequestException as e:
                print(f"An error has occured: {e}")
                raise
        elif method == "DELETE":
            try:
                resp = requests.post(url, headers= headers, timeout=self.timeout)
            except requests.RequestException as e:
                print(f"An error has occured: {e}")
                raise
        content = resp.content
        data = self._parse_data(content if isinstance(content, basestring) else content.decode('utf-8'))
        return data

    def _build_url(self, url, params) -> str:
        if params and len(params) > 0:
            url = url + '?' + self._encode_parameters(params)
        return url

    def _encode_parameters(self, params) -> str:
        if params is None:
            return None
        else:
            params_tuple = []
            for k,v in params.items():
                if v is None:
                    continue
                if isinstance(v, (list,tuple)):
                    for _ in v:
                        params_tuple.append((k,_))
                else:
                    params_tuple.append((k,v))
            return urlencode(params_tuple)

    def _parse_data(self, content):
        try:
            data = json.loads(content)
            self._check_api_error(data)
        except:
            raise    
        return data
    
    def _check_api_error(self, data : dict): 
        if "result" in data.keys():
            if data['result'] == 'error' or 'error' in data:
                raise ApiError(data['errors'])
            if isinstance(data, (list, tuple)) and len(data) > 0:
                if 'error' in data:
                    raise ApiError(data['errors'])

    def _create_manga(self, elem) -> Manga:
        manga = Manga()
        manga._MangaFromDict(elem)
        return manga

    def _create_manga_list(self, resp) -> List[Manga]:
        resp = resp["results"]
        manga_list = []
        for elem in resp:
            manga_list.append(self._create_manga(elem))
        return manga_list

    def _create_tag(self, elem) -> Tag:
        tag = Tag()
        tag._TagFromDict(elem)
        return tag

    def _create_tag_list(self, resp) -> List[Tag]:
        tag_list = []
        for tag in resp:
            tag_list.append(self._create_tag(tag))
        return tag_list

    def _create_chapter(self, elem) -> Chapter:
        chap = Chapter()
        chap._ChapterFromDict(elem)
        return chap

    def _create_chapter_list(self, resp) -> List[Chapter]:
        resp = resp["results"]
        chap_list = []
        for elem in resp:
            chap_list.append(self._create_chapter(elem))
        return chap_list
    
    def _create_author(self, elem) -> Author:
        author = Author()
        author._AuthorFromDict(elem)
        return author

    def _create_authors_list(self, resp) -> List[Author]:
        resp = resp["results"]
        authors_list = []
        for elem in resp:
            authors_list.append(self._create_author(elem))
        return authors_list

    def _create_user(self, elem) -> User:
        user = User()
        user._UserFromDict(elem)
        return user
    
    def _create_user_list(self, resp) -> List[User]:
        resp = resp["results"]
        user_list = []
        for elem in resp:
            user_list.append(self._create_user(elem))

        return user_list

    def _create_group(self, elem) ->  ScanlationGroup:
        group = ScanlationGroup()
        group._ScanlationFromDict(elem)
        return group

    def _create_group_list(self, resp)-> List[ScanlationGroup]:
        resp = resp["results"]
        group_list = []
        for elem in resp:
            group_list.append(self._create_group(elem))
        
        return group_list  

    def get_manga_list(self, **kwargs) -> List[Manga]:
        """
        Search a List of Manga

        Parameters
        -------------
        This parameters may be used by ohter methods
        limit : `int`
        offset : `int`
        title : `str`
        authors : `List[str]`
        artist : `List[str]`
        year : `int`
        includeTags : `List[str]`
        includedTagsMode: `str`. Default `"AND"`. Enum: `"AND"` `"OR"`
        excludedTags : `List[str]`
        exludedTagsMode : `str`. Default `"AND"`, Enum : `"AND"`, `"OR"`
        status : `List[str]`. Items Enum : `"ongoing"`, `"completed"`, `"hiatus"`, `"cancelled"`
        originalLanguage : `List[str]`
        publicationDemographic : `List[str]`. Items Enum: `"shounen"` `"shoujo"` `"josei"` `"seinen"` `"none"`
        ids :  `List[str]`. Limited to 100 per call
        contentRating : `List[str]`. Items Enum : `"safe"` `"suggestive"` `"erotica"` `"pornographic"`
        createdAtSince : `str`. Datetime String with the following format YYYY-MM-DDTHH:MM:SS
        updatedAtSince : `str`. Datetime String with the following format YYYY-MM-DDTHH:MM:SS
        
        Returns
        -------------
        `List[Manga]`. A list of Manga objects

        Raises
        -------------
        `ApiError`

        `MangaError`
        """
        url = f"{self.URL}/manga"
        resp = self._request_url(url, 'GET', params=kwargs)
        return self._create_manga_list(resp)

    def view_manga_by_id(self, id: str)-> Manga:
        """
        Get a Manga by its id

        Parameters
        ------------
        id: `str`. The manga id

        Returns
        -------------
        `Manga`. A Manga object

        Raises
        ------------
        `ApiError`

        `MangaError`
        """
        url = f"{self.URL}/manga/{id}"
        resp = self._request_url(url, "GET")
        return self._create_manga(resp)
    
    def random_manga(self) -> Manga:
        """
        Get a random Manga

        Returns
        ----------
        `Manga`. A Manga object

        Raises
        ----------
        `ApiError`

        `MangaError`
        """
        url = f"{self.URL}/manga/random"
        resp = self._request_url(url, "GET")
        return self._create_manga(resp)
    
    def get_manga_read_markes(self, id : str) -> List[Chapter]: # this needs a performance update
        """
        A list of Chapter Id's That are marked fro the given manga Id
        

        Parameters
        ------------
        id : `str`. The Manga id

        Returns
        -------------
        `List[Chapters]`. A list of chapters that are marked as read
        """
        url = f"{self.URL}/manga/{id}/read"
        resp = self._request_url(url, "GET", headers=self.bearer)
        chap_ids = resp["data"]
        return [self.get_chapter(chap) for chap in chap_ids] # I think this is 

    def tag_list(self) -> List[Tag]:
        """
        Get the list of available tags

        Returns
        ------------
        `List[Tag]`. A list of Tag objects

        Raises
        -----------
        `ApiError`

        `TagError`
        """
        url = f"{self.URL}/manga/tag"
        resp = self._request_url(url, "GET")
        return self._create_tag_list(resp)
    
    def manga_feed(self, id : str, **kwargs) -> List[Chapter]:
        """
        Get the manga feed

        Parameters
        ------------
        
        id `str`, Required. The manga id

        limit : `int`
        offset : `int`
        locales : `List[str]`
        createdAtSince : `str`. Datetime String with the following format YYYY-MM-DDTHH:MM:SS
        updatedAtSince : `str`. Datetime String with the following format YYYY-MM-DDTHH:MM:SS

        Returns
        -------------
        `List[Chapter]` A list of Chapter Objects

        Raises
        -------------
        `ApiError`

        `ChapterError`
        """
        url = f"{self.URL}/manga/{id}/feed"
        resp = self._request_url(url, "GET", params = kwargs)
        return self._create_chapter_list(resp)

    def chapter_list(self, **kwargs) -> List[Chapter]:
        """
        The list of chapters. To get the chpaters of a specific manga the manga parameter must be provided

        Parameters
        -----------
        limit : `int`
        offset : `int`
        title : `str`
        groups : `[str]`
        uploader : `str`    
        manga : `str`
        volume : `str`
        chapter : `str`
        tranlatedLanguaje : `str`
        createdAtSince : `str`. Datetime String with the following format YYYY-MM-DDTHH:MM:SS
        updatedAtSince : `str`. Datetime String with the following format YYYY-MM-DDTHH:MM:SS
        publishAtSince : `str`. Datetime String with the following format YYYY-MM-DDTHH:MM:SS

        Returns
        ----------
        `List[Chpater]` A list of Chpater Objects

        Raises
        -------------
        `ApiError`

        `ChapterError`
        """
        url = f"{self.URL}/chapter"
        resp = self._request_url(url, "GET", params= kwargs)
        return self._create_chapter_list(resp)

    def get_chapter(self, id: str) -> Chapter:
        """
        Get a Chapter by its id


        Parameters
        ------------
        id : `str` The chapter id

        Returns
        ------------
        `Chapter` A chapter Object

        Raises
        ------------
        `ApiError`

        `ChapterError`

        """
        url = f"{self.URL}/chapter/{id}"
        resp = self._request_url(url, "GET")
        return self._create_chapter(resp)
        

    def fetch_chapter_images(self, chapter : Chapter) -> List[str]: #maybe make this an async function?
        """
        Get the image links for a given chapter

        Params
        -----------
        chapter `Chapter`. The chapter 

        Returns
        -----------
        `List[str]`. A list with the links with the chapter images

        NOTE: There links are valid for 15 minutes until you need to renew the token

        Raises
        -----------
        `ApiError`
        """
        url = f"{self.URL}/at-home/server/{chapter.id}"
        image_server_url = self._request_url(url, "GET")
        image_server_url = image_server_url["baseUrl"].replace("\\", "")
        image_server_url = f"{image_server_url}/data"
        image_urls = []
        for filename in chapter.data:
            image_urls.append(f"{image_server_url}/{chapter.hash}/{filename}")

        return image_urls

    def get_author(self, **kwargs) -> Author:
        """
        """
        url = f"{self.URL}/author"
        resp = self._request_url(url, "GET", kwargs)
        return self._create_authors_list(resp)

    def get_author_by_id(self, id : str) -> Author:
        """
        """
        url = f"{self.URL}/author/{id}"
        resp = self._request_url(url, "GET")
        return self._create_author(resp)
    
    def get_user(self, id : str) -> User:
        """
        """
        url = f"{self.URL}/user/{id}"
        resp = self._request_url(url, "GET")
        return self._create_user(resp)

    def login(self, username : str, password : str):
        """
        """
        self._auth_handler(json_payload= {"username" : username, "password" : password})

    def me(self) -> User:
        """
        """
        url = f"{self.URL}/user/me"
        resp = self._request_url(url, "GET", headers= self.bearer)
        return self._create_user(resp)

    def get_my_mangalist(self, **kwargs) -> List[Manga]:
        """
        """
        url = f"{self.URL}/user/follows/manga"
        resp = self._request_url(url, "GET", params = kwargs, headers=self.bearer)
        return self._create_manga_list(resp)
    
    def get_my_followed_groups(self, **kwargs) -> List[ScanlationGroup]:
        """
        """
        url = f"{self.URL}/user/follows/group"
        resp = self._request_url(url, "GET", params=kwargs, headers= self.bearer)
        return self._create_group_list(resp)

    def get_my_followed_users(self, **kwargs) -> List[User]:
        """
        """
        url = f"{self.URL}/user/follows/user"
        resp = self._request_url(url, "GET", params=kwargs, headers=self.bearer)
        return self._create_user_list(resp)
