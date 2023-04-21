---
title: "Understanding GitHub Actions and Ruby Versions for Jekyll: Resolving Compatibility Issues"
date: 2023-04-20
tags: [jekyll, github, ruby, github-actions]
---

*Author's note: I recently encountered an issue with one of my Jekyll projects when using GitHub Actions to build and deploy the site. After some tinkering and research, I discovered how Ruby versions are managed in Jekyll projects and GitHub Actions workflows, and how to resolve compatibility issues. I thought I'd share this knowledge with the community in the hopes it might help someone else.*

## The Issue

I was using the `helaili/jekyll-action@v2` Jekyll GitHub Action from the marketplace to build and deploy my site, and I came across an error in my workflow:

```console
env: can't execute 'ruby-2.7': No such file or directory
```

Later, after some adjustments, I encountered another error:

```console
sass-embedded-1.62.0-x86_64-linux-musl requires rubygems version >= 3.3.22,
which is incompatible with the current version, 3.1.6
```

## The Solution

To fix the compatibility issue with the `sass-embedded` gem, I used the `pre_build_commands` option of the `helaili/jekyll-action@v2` action to update RubyGems before building the site. Here's my final, working GitHub Actions workflow:

```yaml
name: Build and deploy jekyll site

on:
  push:
    branches:
      - main

  workflow_dispatch:

jobs:
  jekyll:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: 📂 setup
        uses: actions/checkout@v3

      - name: 🎁 Cache Ruby gems
        uses: actions/cache@v2
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

The key addition to the workflow is the `pre_build_commands` option:

```yaml
pre_build_commands: 'gem update --system'
```

This command updates RubyGems to the latest version before building the site, which resolves the compatibility issue with the `sass-embedded` gem.

## Conclusion

Understanding how Ruby versions and dependencies are managed in Jekyll projects and GitHub Actions workflows, and how to use the `pre_build_commands` option, helped me fix the issues I encountered and allowed me to continue building and deploying my site smoothly. I hope this post provides some insight for others who may face similar issues. Happy coding!
