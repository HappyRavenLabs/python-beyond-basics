---
name: "📘 Request a new topic"
about: Suggest a new topic to be added to this book
title: "[Topic Request]: "
labels: "enhancement, topic-request"
assignees: "jamesWalczak"
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to propose new topics!
  - type: textarea
    id: what
    attributes:
      label: Topic name?
      description: What topic you want to be covered in the book?
      placeholder: Tell us what you want to learn more!
    validations:
      required: true
---
