# spaCy v3 Project Startup / Transfer

This tool will walk you through creating a simple `project.yml` file for use with [spaCy projects](https://spacy.io/usage/projects).

Note that there are already many excellent templates for starting a project at https://github.com/explosion/projects.  These will probably be what you need most of the time. If one of those fits your need, use them! They contain helpful comments on how the different aspects of the project file works.

My use case was such that none of the templates were a good fit. I had an old NLP project with existing files I was transitioning into spaCy but didn't yet use a spaCy model. I wanted to use the project framework to organize the collection of scripts and data I was already using and delete a gnarly Makefile. I also wanted to play around with [questionary](https://github.com/tmbo/questionary) 🤓

Standard code quality disclaimer: I wrote this in a few hours, so there are no tests. It's also missing a 