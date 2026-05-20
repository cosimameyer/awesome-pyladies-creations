# Welcome!

Thank you for your interest in contributing to **awesome-pyladies-creations**! This repository collects blogs, YouTube channels, podcasts, and Python packages created by PyLadies members from around the world, as well as individual PyLadies members and local chapters. The goal is to make this work more visible and to celebrate the community's contributions.

There are four ways to contribute:
- **Content** (blogs, YouTube channels, podcasts) → add a file to [`data/content/`](data/content/)
- **Python packages** → add a file to [`data/packages/`](data/packages/)
- **Yourself as a PyLadies member** → add a file to [`data/members/`](data/members/)
- **A PyLadies chapter** → add a file to [`data/chapters/`](data/chapters/)

Not sure where to start? [Open an issue](https://github.com/cosimameyer/awesome-pyladies-creations/issues/new/choose) and I'll help you out!

---

# About 

This repository relies heavily on the [Awesome R-Ladies+ blogs repository](https://github.com/rladies/awesome-rladies-blogs), to whom all credit goes. I can only repeat their words and their excellent description of how to submit a new entry below:

It has a similar goal and collects PyLadies blogs. This includes those who identify as a minority gender (including but not limited to cis/trans women, trans men, non-binary, genderqueer, & agender). It would be great to have contributions to this list! If you identify with PyLadies and have a blog, please add yourself.

With your submission, you agree that these entries will be used for the [PyLadies' Mastodon bot](https://botsin.space/@pyladies_bot), which will post (new) PyLadies' blog entries to promote the work of PyLadies around the world. 

# Contributing Checklist

 - [ ] The entry will be added to the [data/content/](data/content/) folder.
 - [ ] The filename of the entry ends with `.json'.
 - [ ] **One file = one piece of content.** If you have both a blog and a YouTube channel (or a podcast), please add a separate file for each. The same author can appear in multiple files.
 - [ ] The json contains at least
     - [ ] title (title of the content)
     - [ ] type (one of `"blog"`, `"youtube"`, `"podcast"`)
     - [ ] url (URL of the content)
     - [ ] rss_feed (RSS feed for the content; required if you want it promoted by the Mastodon/Bluesky bot. For a `youtube` entry this is the channel/playlist feed; for a `blog` entry this is your blog's Python-related feed; for a `podcast` entry this is the podcast feed.)
     - [ ] photo_url (logo or profile)
     - [ ] language (one of the [ISO 639-1 language codes](https://www.w3schools.com/tags/ref_language_codes.asp))
     - [ ] authors (list of authors)

# Contribution Details

All content is listed in the [data/content/](data/content/) folder, where each piece of content lives in its own json file. One file describes one blog, one YouTube channel, or one podcast — never several at once. If a contributor has both a blog and a YouTube channel, they will have two files. Follow the instructions below to add to the list. If you have any problems, please create an issue so we can help you.

Depending on how you are most comfortable, there are several ways to add new entries. 

## Option 1: Not Too Familiar with JSON/GitHub?

If you're not familiar with JSON, open a pre-filled issue and I'll create the JSON for you!

- [Add a blog](https://github.com/cosimameyer/awesome-pyladies-creations/issues/new?title=New%20entry%3A%20%5Bblog%5D%20%3CBlog%20Name%3E&body=%2A%2ABlog%20name%2A%2A%3A%20%0A%2A%2AURL%2A%2A%3A%20%0A%2A%2ARSS%20feed%2A%2A%20%28optional%20%E2%80%94%20a%20Python-specific%20feed%20is%20preferred%20if%20available%29%3A%20%0A%2A%2AAuthor%20name%2A%2A%3A%20%0A%2A%2ALanguage%2A%2A%20%28ISO%20639-1%2C%20e.g.%20%60en%60%29%3A%20%0A%2A%2ASocial%20media%2A%2A%20%28GitHub%2C%20Twitter/X%2C%20Mastodon%2C%20LinkedIn%2C%20etc.%29%3A%20%0A)
- [Add a YouTube channel](https://github.com/cosimameyer/awesome-pyladies-creations/issues/new?title=New%20entry%3A%20%5Byoutube%5D%20%3CChannel%20Name%3E&body=%2A%2AChannel%20name%2A%2A%3A%20%0A%2A%2AURL%2A%2A%3A%20%0A%2A%2ARSS%20feed%2A%2A%20%28channel%20or%20playlist%20feed%20URL%29%3A%20%0A%2A%2AAuthor/organizer%20name%2A%2A%3A%20%0A%2A%2ALanguage%2A%2A%20%28ISO%20639-1%2C%20e.g.%20%60en%60%29%3A%20%0A%2A%2ASocial%20media%2A%2A%20%28GitHub%2C%20Twitter/X%2C%20Mastodon%2C%20LinkedIn%2C%20etc.%29%3A%20%0A)
- [Add a podcast](https://github.com/cosimameyer/awesome-pyladies-creations/issues/new?title=New%20entry%3A%20%5Bpodcast%5D%20%3CPodcast%20Name%3E&body=%2A%2APodcast%20name%2A%2A%3A%20%0A%2A%2AURL%2A%2A%3A%20%0A%2A%2ARSS%20feed%2A%2A%3A%20%0A%2A%2AHost/author%20name%2A%2A%3A%20%0A%2A%2ALanguage%2A%2A%20%28ISO%20639-1%2C%20e.g.%20%60en%60%29%3A%20%0A%2A%2ASocial%20media%2A%2A%20%28GitHub%2C%20Twitter/X%2C%20Mastodon%2C%20LinkedIn%2C%20etc.%29%3A%20%0A)
- [Add a Python package](https://github.com/cosimameyer/awesome-pyladies-creations/issues/new?title=New%20entry%3A%20%5Bpackage%5D%20%3CPackage%20Name%3E&body=%2A%2APackage%20name%2A%2A%3A%20%0A%2A%2APyPI%20URL%2A%2A%3A%20%0A%2A%2ARepository%20URL%2A%2A%3A%20%0A%2A%2AMaintainer%20name%28s%29%2A%2A%3A%20%0A%2A%2ASocial%20media%2A%2A%20%28GitHub%2C%20etc.%29%3A%20%0A)
- [Add yourself as a member](https://github.com/cosimameyer/awesome-pyladies-creations/issues/new?title=New%20entry%3A%20%5Bmember%5D%20%3CYour%20Name%3E&body=%2A%2AName%2A%2A%3A%20%0A%2A%2APhoto%20URL%2A%2A%20%28optional%29%3A%20%0A%2A%2ASocial%20media%2A%2A%20%28GitHub%2C%20Twitter%2FX%2C%20Mastodon%2C%20LinkedIn%2C%20etc.%29%3A%20%0A)
- [Add a PyLadies chapter](https://github.com/cosimameyer/awesome-pyladies-creations/issues/new?title=New%20entry%3A%20%5Bchapter%5D%20%3CChapter%20Name%3E&body=%2A%2AChapter%20name%2A%2A%3A%20%0A%2A%2ACity%2A%2A%3A%20%0A%2A%2ACountry%2A%2A%3A%20%0A%2A%2AEmail%2A%2A%20%28optional%29%3A%20%0A%2A%2AWebsite%2A%2A%20%28optional%29%3A%20%0A%2A%2ASocial%20media%2A%2A%20%28GitHub%2C%20Twitter%2FX%2C%20Instagram%2C%20Meetup%2C%20etc.%29%3A%20%0A)

## Option 2: Create a New File

### For General Content (Blog, YouTube, Podcast)
Create a new file in the [data/content/](data/content/) folder by [using this link](https://github.com/cosimameyer/awesome-pyladies-creations/new/main/?filename=data/content/your-blog-url.com.json&value=%7B%0A%20%20%22title%22%3A%20%22Your%20title%22%2C%20//required%0A%20%20%22subtitle%22%3A%20%22subtitle%20or%20tagline%22%2C%20//optional%0A%20%20%22type%22%3A%20%22blog%22%2C%20//required%3A%20one%20of%20%22blog%22%2C%20%22youtube%22%2C%20%22podcast%22%0A%20%20%22url%22%3A%20%22https%3A//your_blog.com%22%2C%20//required%0A%20%20%22photo_url%22%3A%20%22https%3A//your_blog.com/your_photo.png%22%2C%20//required%0A%20%20%22description%22%3A%20%22Short%20description%20of%20what%20you%20blog%20about%22%2C%0A%20%20%22language%22%3A%20%22en%22%2C%20//required%0A%20%20%22rss_feed%22%3A%20%22%5Burl%5D/file.xml%22%2C%20//required%20if%20you%20want%20your%20feed%20to%20be%20promoted%20by%20the%20bot%0A%20%20%22authors%22%3A%20%5B%20//required%0A%20%20%20%20%7B%0A%20%20%20%20%20%20%22name%22%3A%20%22Your%20Name%22%2C%20//required%0A%20%20%20%20%20%20%22social_media%22%3A%20%5B%7B%0A%20%20%20%20%20%20%20%20%20%22twitter%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22mastodon%22%3A%20%22%40username%40server.org%22%2C%0A%20%20%20%20%20%20%20%20%20%22bluesky%22%3A%20%22%40username.bsky.social%22%2C%0A%20%20%20%20%20%20%20%20%20%22github%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22instagram%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22youtube%22%3A%20%22username/end-url%22%2C%0A%20%20%20%20%20%20%20%20%20%22tiktok%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22website%22%3A%20%22url%22%2C%0A%20%20%20%20%20%20%20%20%20%22linkedin%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22facebook%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22orcid%22%3A%20%22member%20number%22%2C%0A%20%20%20%20%20%20%20%20%20%22meetup%22%3A%20%22end-url%22%0A%20%20%20%20%20%20%7D%5D%0A%20%20%20%20%7D%0A%20%20%5D%0A%7D).

This link will fork the repository to your user account, and initiate a new file with some template content in it. After filling the file, please [create a PR to the main branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

#### File Name

The name of the file should be the URL of the content itself, without `www` or `http(s)://`. This way each file has a unique name and we avoid duplicates.

- For a blog: use the blog's domain, e.g. `cosimameyer.com.json`.
- For a YouTube channel: use the channel URL, e.g. `youtube.com.@PyLadiesBerlin.json`.
- For a podcast: use the podcast feed/landing-page URL.

If the same person has both a blog and a YouTube channel, they get **two files** — one for each — and the same `authors` block can appear in both.

#### File Content

Using the link above will create a template for you to start with.
Fill inn all the information that is relevant for your blog.
There are several adaptations to an entry you can make that are not highlighted in every entry.
Remove all mentions of `\\required`, these are just for making it clear which information you _must_ provide for the file to be valid.
Any optional field you don't want to add, you may delete entirely.
For instance, if you don't have a subtitle or tagline for your blog, remove the entire line of `"subtite": "subtitle or tagline"` rather than leaving it empty with `"subtite": ""`

##### Photo

The photo url you provide will be displayed as your blogs thumbnail. 
This may be a picture of you, or if you have a logo for your blog/website, it may be best to use this in stead.


##### RSS Feed

The single `rss_feed` field is used for every content type — the bot picks the right behavior based on `type`.

- For `type: "blog"`: a feed of your Python-related posts (a category/tag feed is best; a title-filtered feed works too).
- For `type: "youtube"`: the YouTube channel or playlist feed (see ["RSS feed for YouTube videos"](#rss-feed-for-youtube-videos) below).
- For `type: "podcast"`: the podcast's RSS feed.

For blog feeds specifically, ideally you have a Python-only feed. A title-based RSS feed is fine.

Depending on how your website is set up, the implementation may differ. If you need more input on how to get your RSS, have a look [here](https://zapier.com/blog/how-to-find-rss-feed-url/). If you want to check how your RSS looks like, you can use [simple pie](https://simplepie.org/demo/). We collected a few of the most common approaches below: 

<details markdown="1"><summary>Quarto</summary>

- Change the code in `index.qmd` as (under listing, also described [here](https://quarto.org/docs/websites/website-blog.html#rss-feed)):

  ```
  feed:
    categories: [Python]
  ```

- Note to new users that the category names will be the names of your category tags used in the blogs (not `posts`, which are the posts folder for Quarto blogs)
- Then provide the RSS feed links as, `[url]/blog/index-r.xml` for R category posts (`[url]/blog/index.xml` will be the RSS feed link for main posts only)

</details>

<details markdown="1"><summary>Distill</summary>

There is currently a [workaround](https://github.com/rladies/awesome-rladies-creations/pull/54#issuecomment-1501263818) for adding RSS feeds in distill (from the R-Ladies+ repo) that works as follows:

- In distill, there is a categories folder generated when a post is rendered which gets deleted when the blog is rendered
- Store the folder and add it later because we need a categories folder, containing each specified category with an `index.xml` for each category

</details>

<details markdown="1"><summary>Hugo</summary>

#### Hugo Academic

- Apparently the RSS feed is enabled by default and you can access it by using the field `category` in the YAML of your posts
- Further readings for [Hugo Academic](https://cosimameyer.com/post/adding-your-hugo-academic-blog-to-r-bloggers-and-python-bloggers/)

#### Hugo Portio

- Copy and paste the content of [this file](https://github.com/gohugoio/hugo/blob/master/tpl/tplimpl/embedded/templates/_default/rss.xml) (it’s Hugo’s default RSS settings)
- Store it under `layouts/_default/rss.xml` (if there is no file, you need to create this one).
- Exchange one line. Instead of `<description>{{ .Summary | html }}</description>`, we want `<description>{{ .Content | html }}</description>` (it’s at the very bottom of the file). This way, you RSS feed doesn’t show an excerpt but the full text.
- More about [Hugo Portio](https://cosimameyer.com/post/adding-your-hugo-academic-blog-to-r-bloggers-and-python-bloggers/)

</details>

<details markdown="1"><summary>Medium</summary>

Medium nicely describes on their website how to [get your RSS feed](https://help.medium.com/hc/en-us/articles/214874118-Using-RSS-feeds-of-profiles-publications-and-topics). Unfortunately it’s not possible to have a tag specific feed (yet). To keep the bot sorted, please make sure to only post about Python-related topics (= things that could be interesting to the followers of the bot).

</details>

##### RSS feed for YouTube videos

For a YouTube entry, set `type: "youtube"` and put the channel or playlist feed URL in `rss_feed`. You first need to get your channel or playlist ID. How to get them is described [here](https://www.youtube.com/watch?v=vdk8dx08ExU).
Assemble the feed URL together with the base URL:

- For *channels*: `https://www.youtube.com/feeds/videos.xml?channel_id=` + `CHANNEL_ID`
- For *playlists*: `https://www.youtube.com/feeds/videos.xml?playlist_id=` + `PLAYLIST_ID`

### For Python Libraries

Create a new file in the [data/content/](data/content/) folder by [using this link](https://github.com/cosimameyer/awesome-pyladies-creations/new/main/?filename=data/packages/your-package-name.json&value=%7B%0A%20%20%22name%22%3A%20%22Your%20title%22%2C%20%2F%2Frequired%0A%20%20%22description%22%3A%20%22Short%20description%20of%20what%20you%20package%20is%20about%22%2C%0A%20%20%22logo_url%22%3A%20%22https%3A%2F%2Fgithub.com%2Fusername%2Fpackage%2Fman%2Flogo.png%22%0A%20%20%22repo_url%22%3A%20%22https%3A%2F%2Fgithub.com%2Fusername%2Fpackage%22%2C%0A%20%20%22pypi_url%3A%20%22https%3A%2F%2Fpypi.site%22%2C%0A%20%20%22maintainers%22%3A%20%5B%20%2F%2Frequired%0A%20%20%20%20%7B%0A%20%20%20%20%20%20%22name%22%3A%20%22Your%20Name%22%2C%20%2F%2Frequired%0A%20%20%20%20%20%20%22social_media%22%3A%20%5B%7B%0A%20%20%20%20%20%20%20%20%20%22twitter%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22mastodon%22%3A%20%22%40username%40server.org%22%2C%0A%20%20%20%20%20%20%20%20%20%22bluesky%22%3A%20%22username.domain%22%2C%0A%20%20%20%20%20%20%20%20%20%22github%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22instagram%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22youtube%22%3A%20%22username%2Fend-url%22%2C%0A%20%20%20%20%20%20%20%20%20%22tiktok%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22periscope%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22researchgate%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22website%22%3A%20%22url%22%2C%0A%20%20%20%20%20%20%20%20%20%22linkedin%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22facebook%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22orcid%22%3A%20%22member%20number%22%2C%0A%20%20%20%20%20%20%20%20%20%22meetup%22%3A%20%22end-url%22%0A%20%20%20%20%20%20%7D%5D%0A%20%20%20%20%7D%0A%20%20%5D%0A%7D)

### For Members

If you are a PyLadies member and want to appear in the directory, create a new file in the [data/members/](data/members/) folder. Name the file after yourself, e.g. `jane-doe.json`.

```json
{
  "name": "Your Name",
  "photo_url": "https://example.com/your_photo.png",
  "social_media": [{
    "github": "username",
    "twitter": "username",
    "mastodon": "@username@server.org",
    "bluesky": "@username.bsky.social",
    "linkedin": "username",
    "instagram": "username",
    "website": "https://yoursite.com"
  }]
}
```

**Required fields:** `name`  
**Optional fields:** `photo_url`, `social_media` (any combination of platforms)

### For PyLadies Chapters

To add or update a PyLadies chapter, create a new file in the [data/chapters/](data/chapters/) folder. Name the file after the chapter city/region, e.g. `berlin.json`.

```json
{
  "name": "PyLadies Berlin",
  "city": "Berlin",
  "country": "Germany",
  "lat": 52.52,
  "lon": 13.405,
  "website": "https://berlin.pyladies.com",
  "email": "berlin@pyladies.com",
  "photo_url": "https://example.com/chapter_logo.png",
  "social_media": [{
    "github": "pyladies-berlin",
    "twitter": "PyLadiesBerlin",
    "mastodon": "@pyladiesberlin@fosstodon.org",
    "bluesky": "@pyladiesberlin.bsky.social",
    "instagram": "pyladiesberlin",
    "linkedin": "company/pyladies-berlin",
    "meetup": "PyLadies-Berlin",
    "facebook": "PyLadiesBerlin",
    "youtube": "@PyLadiesBerlin",
    "website": "https://berlin.pyladies.com"
  }]
}
```

**Required fields:** `name`, `city`, `country`  
**Optional fields:** `lat`/`lon` (decimal coordinates), `website`, `email`, `photo_url`, `social_media`

#### Chapter YouTube / Blog entries

If your chapter has a YouTube channel or blog, you can also add a content entry in `data/content/` (following the General Content format above). Add `"chapter": true` at the top level of that file so the site knows to show it in the chapters section rather than as an individual creator:

```json
{
  "title": "PyLadies Berlin",
  "type": "youtube",
  "url": "https://www.youtube.com/@PyLadiesBerlin",
  "chapter": true,
  "authors": [{ "name": "PyLadies Berlin", "social_media": [{ ... }] }]
}
```

The chapter card will appear in the Chapters section and will be enriched with the content entry's data (photo, social links, RSS feed for the bot).

## General Remarks

#### Authors

The entry may have several authors. This is for blogs where maybe there are several blogging together. If it is a blog that mainly has guest bloggers, its better to list the editors/maintainers of the blog and add "guest bloggers" as authors also.

Adding several authors means duplicating the content between the curlies `{}` in the author section, and adding a comma between each one.

```json
"authors": [
  {
    "name": "Athanasia Mo  Mowinckel",
    "social_media": [{
      "twitter": "DrMowinckels",
      "github": "Athanasiamo"
    }]
  },
  {
    "name": "Mary Johnson",
    "social_media": [{
      "linkedin": "maryj",
      "youtube": "maryj"
    }]
  },
  {
    "name": "Guest bloggers"
  }
]
```

#### Social Media

```json
"twitter": "username"
"mastodon": "@username@instance"
"github": "username"
"instagram": "username"
"youtube": "username/end-url"
"tiktok": "username"
"periscope": "username"
"researchgate": "username"
"website": "url"
"linkedin": "username"
"facebook": "username"
"orcid": "member number"
"meetup": "end-url"
```

#### Language
The language field should be populated with the [ISO 639-1 Language Codes](https://www.w3schools.com/tags/ref_language_codes.asp) of the site content.
Please be thorough when entering this information.

#### Help Needed?

If there is help needed, feel free to reach out to [me directly](mailto:contact@cosimameyer.com).
