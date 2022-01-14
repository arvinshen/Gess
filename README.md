<div id="top"></div>

<!-- PROJECT SHIELDS -->

<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/arvinshen/Gess">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Gess</h3>

  <p align="center">
    <a href="https://github.com/arvinshen/Gess"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/arvinshen/Gess">View Demo</a>
    ·
    <a href="https://github.com/arvinshen/Gess/issues">Report Bug</a>
    ·
    <a href="https://github.com/arvinshen/Gess/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

Gess is an abstract strategy board game that is a combination of two popular games - "Chess" and "Go".

### Rules

Black goes first. Each piece consists of a 3x3 grid. The central square determines the extent of the piece's move and all of it's stones in its footprint move in unison. When a piece's move causes it to overlap stones, any stones covered by the footprint get removed, not just those covered by one of the piece's stones.
It's possible for a player to have more than one ring. A player doesn't lose until they have no remaining rings.

Locations on the board are specified using columns labeled a-t and rows labeled 1-20,
with row 1 being the Black side and row 20 the White side. The actual board is only columns b-s and rows 2-19. An edge of the piece may go into columns a or t, or rows 1 or 20, but any pieces there are removed at the end of the move.

There are many variations of Gess. While some variations it is not legal to make a move that leaves you without a ring, in this variation it is legal (although not a recommended move obviously).

For a full explanation, check out the [rules](https://www.wikiwand.com/en/Gess).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

Follow these simple steps to get a local copy up and running.

### Prerequisites

This project uses [python](https://www.python.org/). Check to see if you have python installed locally before proceeding.

### Installation

1.  Clone the repo
    ```sh
    git clone https://github.com/arvinshen/Gess.git
    ```

### Usage

2.  Open GessGame.py

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See [LICENSE][license-url] for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Project Link: <https://github.com/arvinshen/Gess>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/arvinshen/Gess.svg?style=for-the-badge

[contributors-url]: https://github.com/arvinshen/Gess/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/arvinshen/Gess.svg?style=for-the-badge

[forks-url]: https://github.com/arvinshen/Gess/network/members

[stars-shield]: https://img.shields.io/github/stars/arvinshen/Gess.svg?style=for-the-badge

[stars-url]: https://github.com/arvinshen/Gess/stargazers

[issues-shield]: https://img.shields.io/github/issues/arvinshen/Gess.svg?style=for-the-badge

[issues-url]: https://github.com/arvinshen/Gess/issues

[license-shield]: https://img.shields.io/github/license/arvinshen/Gess.svg?style=for-the-badge

[license-url]: https://github.com/arvinshen/Gess/blob/master/LICENSE.txt

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555

[linkedin-url]: https://linkedin.com/in/linkedin_username
