---
layout: post
title: "Building a Cost-Effective, Hassle-Free Website for a Tattoo Studio"
date: 2023-04-22
tags: [DevOps, Jekyll, GitHub Pages]
---

## The Issue

A non-tech-savvy friend of mine recently decided to open a tattoo studio. I offered to build and host a website for his new venture with minimal cost, maintenance, and coding effort. In this post, I'll share how I set up a mobile-friendly, SEO-optimized, single-scrolling landing page that makes it easy for customers to get in touch and complies with German law.

First, I registered the TLD brotherhood.ink, which was available and perfectly suited for a tattoo studio. The site needed to serve as a landing page, featuring a simple contact form, a list of offered services, and owner information. Ideally, the site would also integrate the artist's Instagram feed, filtering by specific hashtags to keep content fresh and relevant.

## The Solution

To achieve this, I chose [GitHub Pages](https://pages.github.com/) as a free, highly available hosting platform, and [Jekyll](https://jekyllrb.com/) as a static site generator. I configured the domain's DNS to point to GitHub Pages and set up the repository accordingly.

I found a free theme that met our requirements: [Agency Jekyll Theme](https://github.com/y7kim/agency-jekyll-theme). I cloned the theme's repository into a "jekyll" subfolder within our project root, which simplified the deployment process.

Next, I created a Gemfile to list the required Ruby Gems like Jekyll and some additional helpful gems:

```ruby
source 'https://rubygems.org'
gem 'jekyll'
gem 'jekyll-paginate'
gem 'jekyll-sitemap'
gem 'jekyll-feed'
gem 'jekyll-seo-tag'
```

I also added a GitHub workflow that automates the process of building and deploying the Jekyll site to the gh-pages branch whenever changes are pushed to the main branch or a manual dispatch is triggered. The workflow caches Ruby gems and uses the [jekyll-action](https://github.com/helaili/jekyll-action) to build and deploy the site.

```yaml
name: Build and deploy to branch gh-pages

on:
  push:
    branches:
      - main

  workflow_dispatch:

jobs:
  build-and-deploy-jekyll-src-to-branch-gh-pages:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: 📂 setup
        uses: actions/checkout@v3

      - name: 🎁 Cache Ruby gems
        uses: actions/cache@v3
        with:
          path: vendor/bundle
          key: ${{ runner.os }}-gems-${{ hashFiles('**/Gemfile.lock') }}
          restore-keys: |
            ${{ runner.os }}-gems-

      - name: 🚀 Build and deploy
        uses: helaili/jekyll-action@v2
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          jekyll_src: 'jekyll'
          target_branch: 'gh-pages'
          pre_build_commands: 'gem update --system'
```

After configuring the deployment branch and enabling HTTPS, I navigated to <https://brotherhood.ink> and saw the theme's default look. I then replaced the stock content with the actual business information, tweaked the layout, and replaced the header image.

## Conclusion

There's still work to be done, such as integrating the Instagram feed, utilizing the installed Jekyll plugins like jekyll-seo-tag, setting up Google Analytics, configuring a mail server, and more. Stay tuned for updates!

Here's a list of the technologies utilized:

- [GitHub Pages](https://pages.github.com/)
- [Jekyll](https://jekyllrb.com/)
- [Agency Jekyll Theme](https://github.com/y7kim/agency-jekyll-theme)
- [Jekyll SEO Tag](https://github.com/jekyll/jekyll-seo-tag)
- [Jekyll Sitemap](https://github.com/jekyll/jekyll-sitemap)
- [Jekyll Feed](https://github.com/jekyll/jekyll-feed)
- [Jekyll Paginate](https://github.com/jekyll/jekyll-paginate)

This project demonstrates how to create a cost-effective, low-maintenance website using open-source technologies and free hosting services. If you're looking for a similar solution, give it a try!
