Two parts:

1. scrape ct gov webpages for vote data, format the data, put it in a public github repository

   - determine how each representative voted (yay, nay, not present, ...?)

2. given a user's email address and zip code, whenever a new item is available, send them an email showing them the data

Most general need: make user aware when their representative does something that ought to represent them

Minimally viable product: Assume that when a representative votes, data will be posted to a URL. Determine whether or not a new vote has occurred (boolean), and if so, send an email to the user with a URL (link) to the vote data.
