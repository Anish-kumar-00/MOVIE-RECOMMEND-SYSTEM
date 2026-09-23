import gzip
import os
import pickle
import requests
import html
import streamlit as st


# ============================================================
# 1. PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 2. GLOBAL CSS
# ============================================================

st.html("""
<style>

* {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    background: #03030a;
}

.stApp {
    background:
        radial-gradient(circle at 0% 20%, rgba(0, 75, 255, 0.25), transparent 30%),
        radial-gradient(circle at 100% 30%, rgba(255, 0, 60, 0.25), transparent 32%),
        radial-gradient(circle at 50% 100%, rgba(100, 0, 255, 0.15), transparent 35%),
        #03030a;

    color: white;
    overflow-x: hidden;
}

.block-container {
    max-width: 1500px;
    padding-top: 25px;
    padding-bottom: 50px;
}

[data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}


/* ============================================================
   SELECT BOX
   ============================================================ */

div[data-baseweb="select"] > div {
    background: linear-gradient(
        135deg,
        rgba(0, 20, 50, 0.95),
        rgba(25, 0, 25, 0.95)
    ) !important;

    border: 2px solid transparent !important;
    border-radius: 12px !important;
    color: white !important;

    box-shadow:
        0 0 10px rgba(0, 110, 255, 0.25),
        0 0 10px rgba(255, 0, 60, 0.18) !important;
}

div[data-baseweb="select"] > div:focus-within {
    border-color: #008cff !important;

    box-shadow:
        0 0 15px rgba(0, 140, 255, 0.65),
        0 0 25px rgba(255, 0, 80, 0.35) !important;
}


/* ============================================================
   BUTTON
   ============================================================ */

.stButton > button {
    background: linear-gradient(
        135deg,
        #006cff,
        #7b00ff,
        #ff003c
    ) !important;

    color: white !important;

    border: 1px solid #ff174f !important;
    border-radius: 10px !important;

    font-weight: 800 !important;

    transition: all 0.3s ease !important;

    box-shadow:
        0 0 12px rgba(0, 110, 255, 0.25),
        0 0 12px rgba(255, 0, 70, 0.20) !important;
}

.stButton > button:hover {
    transform: translateY(-3px);

    box-shadow:
        0 0 18px rgba(0, 110, 255, 0.60),
        0 0 30px rgba(255, 0, 70, 0.50) !important;
}


/* ============================================================
   HR
   ============================================================ */

hr {
    border: none !important;
    height: 1px !important;

    background: linear-gradient(
        90deg,
        transparent,
        #006cff,
        #ff0066,
        transparent
    ) !important;

    box-shadow: 0 0 10px rgba(0, 100, 255, 0.5);
}


/* ============================================================
   HERO
   ============================================================ */

.hero-box {
    position: relative;

    min-height: 390px;

    display: flex;
    align-items: flex-end;

    padding: 55px;

    border-radius: 20px;

    overflow: hidden;

    background:
        radial-gradient(
            circle at 75% 45%,
            rgba(0, 100, 255, 0.30),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 55%,
            rgba(255, 0, 70, 0.28),
            transparent 30%
        ),
        linear-gradient(
            110deg,
            #02030a,
            #080814,
            #11030a
        );

    border: 2px solid transparent;
    background-clip: padding-box;

    box-shadow:
        0 0 15px rgba(0, 110, 255, 0.45),
        0 0 30px rgba(255, 0, 70, 0.30);

    margin-bottom: 40px;

    animation: heroPulse 4s ease-in-out infinite;
}

.hero-box::before {
    content: "";

    position: absolute;
    inset: 0;

    border-radius: 20px;
    padding: 2px;

    background: linear-gradient(
        90deg,
        #006cff,
        #00c8ff,
        #9d00ff,
        #ff0066,
        #ff1744,
        #006cff
    );

    background-size: 300% 100%;

    animation: neonBorder 5s linear infinite;

    -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);

    -webkit-mask-composite: xor;
    mask-composite: exclude;

    pointer-events: none;
}

.hero-box::after {
    content: "";

    position: absolute;

    width: 450px;
    height: 450px;

    right: -100px;
    top: -120px;

    background: radial-gradient(
        circle,
        rgba(0, 100, 255, 0.25),
        transparent 65%
    );

    filter: blur(25px);

    animation: heroLight 5s ease-in-out infinite;
}

@keyframes heroPulse {

    0% {
        box-shadow:
            0 0 15px rgba(0, 110, 255, 0.35),
            0 0 20px rgba(255, 0, 70, 0.20);
    }

    50% {
        box-shadow:
            0 0 30px rgba(0, 110, 255, 0.65),
            0 0 45px rgba(255, 0, 70, 0.45);
    }

    100% {
        box-shadow:
            0 0 15px rgba(0, 110, 255, 0.35),
            0 0 20px rgba(255, 0, 70, 0.20);
    }
}

@keyframes neonBorder {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

@keyframes heroLight {

    0% {
        transform: translateX(0) translateY(0);
    }

    50% {
        transform: translateX(-100px) translateY(50px);
    }

    100% {
        transform: translateX(0) translateY(0);
    }
}

.hero-content {
    position: relative;
    z-index: 5;

    animation: titleFade 1s ease-out;
}

@keyframes titleFade {

    from {
        opacity: 0;
        transform: translateY(25px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero-title {

    font-size: clamp(38px, 6vw, 72px);

    font-weight: 950;

    line-height: 0.98;

    margin: 10px 0 20px;

    color: white;

    text-shadow:
        0 0 15px rgba(255,255,255,0.15);
}

.gradient-text {

    background: linear-gradient(
        90deg,
        #00aaff,
        #7b00ff,
        #ff0077
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    background-clip: text;
}


/* ============================================================
   SECTION
   ============================================================ */

.section-title {

    font-size: 32px;

    font-weight: 950;

    margin-top: 15px;

    margin-bottom: 5px;

    background: linear-gradient(
        90deg,
        #ffffff 0%,
        #00aaff 35%,
        #9d00ff 65%,
        #ff0066 100%
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    background-clip: text;
}

.section-subtitle {

    color: #aeb4c5;

    margin-bottom: 25px;

    font-size: 15px;
}


/* ============================================================
   SELECTED MOVIE
   ============================================================ */

.selected-movie-box {

    position: relative;

    display: flex;

    align-items: center;

    gap: 28px;

    padding: 18px;

    min-height: 180px;

    margin-top: 25px;

    margin-bottom: 30px;

    border-radius: 18px;

    background: linear-gradient(
        110deg,
        rgba(0, 40, 90, 0.48),
        rgba(25, 5, 50, 0.42),
        rgba(80, 0, 25, 0.45)
    );

    border: 2px solid transparent;

    background-clip: padding-box;

    box-shadow:
        0 0 18px rgba(0, 100, 255, 0.35),
        0 0 30px rgba(255, 0, 70, 0.25);

    overflow: hidden;
}

.selected-movie-box::before {

    content: "";

    position: absolute;

    inset: 0;

    border-radius: 18px;

    padding: 2px;

    background: linear-gradient(
        90deg,
        #0077ff,
        #00ccff,
        #9d00ff,
        #ff0066,
        #ff003c,
        #0077ff
    );

    background-size: 300% 100%;

    animation: neonBorder 4s linear infinite;

    -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);

    -webkit-mask-composite: xor;

    mask-composite: exclude;

    pointer-events: none;
}

.selected-poster {

    width: 120px;
    height: 175px;

    object-fit: cover;

    border-radius: 12px;

    position: relative;

    z-index: 2;

    box-shadow:
        0 0 12px rgba(0, 110, 255, 0.65),
        0 0 20px rgba(255, 0, 70, 0.35);
}

.selected-info {

    position: relative;

    z-index: 2;
}

.selected-badge {

    display: inline-block;

    padding: 5px 12px;

    border-radius: 50px;

    color: white;

    font-size: 12px;

    font-weight: 800;

    background: linear-gradient(
        90deg,
        #006cff,
        #8b00ff,
        #ff0066
    );

    box-shadow:
        0 0 12px rgba(0, 120, 255, 0.45);
}

.selected-title {

    font-size: 32px;

    font-weight: 900;

    margin: 8px 0;
}

.selected-overview {

    color: #c5cad5;

    line-height: 1.6;

    max-width: 750px;
}


/* ============================================================
   MOVIE CARDS
   ============================================================ */

div[data-testid="stHorizontalBlock"] {

    position: relative;

    padding: 7px 4px;

    border-radius: 18px;

    background:
        radial-gradient(
            circle at 0% 50%,
            rgba(0, 100, 255, 0.25),
            transparent 23%
        ),
        radial-gradient(
            circle at 100% 50%,
            rgba(255, 0, 70, 0.25),
            transparent 23%
        );

    margin-bottom: 8px;

    overflow: visible;
}

.movie-wrapper {

    position: relative;

    background: linear-gradient(
        145deg,
        #0d1425,
        #0a0a12
    );

    border: 2px solid transparent;

    border-radius: 14px;

    padding: 5px;

    margin-bottom: 18px;

    overflow: hidden;

    transition:
        transform 0.35s ease,
        box-shadow 0.35s ease;

    box-shadow:
        0 5px 15px rgba(0,0,0,0.5);

    z-index: 2;
}

.movie-wrapper::before {

    content: "";

    position: absolute;

    inset: -2px;

    border-radius: 15px;

    padding: 2px;

    background: linear-gradient(
        130deg,
        #006cff,
        #00c8ff,
        #7000ff,
        #ff0066,
        #ff1744,
        #006cff
    );

    background-size: 350% 350%;

    animation: cardLightning 3.5s linear infinite;

    -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);

    -webkit-mask-composite: xor;

    mask-composite: exclude;

    opacity: 0.95;

    pointer-events: none;
}

@keyframes cardLightning {

    0% {
        background-position: 0% 50%;
    }

    25% {
        background-position: 50% 0%;
    }

    50% {
        background-position: 100% 50%;
    }

    75% {
        background-position: 50% 100%;
    }

    100% {
        background-position: 0% 50%;
    }
}

.movie-wrapper::after {

    content: "";

    position: absolute;

    inset: 0;

    border-radius: 14px;

    background:
        linear-gradient(
            120deg,
            rgba(0, 100, 255, 0.08),
            transparent 35%,
            rgba(255, 0, 70, 0.08)
        );

    pointer-events: none;
}

.movie-wrapper:hover {

    transform:
        translateY(-9px)
        scale(1.035);

    box-shadow:
        0 0 15px rgba(0, 110, 255, 0.65),
        0 0 25px rgba(255, 0, 70, 0.55),
        0 18px 40px rgba(0,0,0,0.75);

    z-index: 50;
}

.movie-poster-container {

    position: relative;

    overflow: hidden;

    border-radius: 9px;

    z-index: 3;
}

.movie-poster {

    width: 100%;

    aspect-ratio: 2 / 3;

    object-fit: cover;

    display: block;

    transition:
        transform 0.55s ease,
        filter 0.55s ease;
}

.movie-wrapper:hover .movie-poster {

    transform: scale(1.08);

    filter:
        brightness(0.48)
        saturate(1.2);
}

.movie-overlay {

    position: absolute;

    inset: 0;

    display: flex;

    align-items: center;

    justify-content: center;

    opacity: 0;

    background:
        linear-gradient(
            to bottom,
            rgba(0,0,0,0.05),
            rgba(0,0,0,0.88)
        );

    transition: opacity 0.35s ease;
}

.movie-wrapper:hover .movie-overlay {

    opacity: 1;
}

.play-circle {

    width: 60px;
    height: 60px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 50%;

    background:
        linear-gradient(
            135deg,
            #006cff,
            #8b00ff,
            #ff003c
        );

    color: white;

    font-size: 24px;

    box-shadow:
        0 0 15px rgba(0, 110, 255, 0.8),
        0 0 30px rgba(255, 0, 70, 0.65);

    animation: playPulse 1.7s infinite;
}

@keyframes playPulse {

    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.08);
    }

    100% {
        transform: scale(1);
    }
}

.movie-title {

    position: relative;

    z-index: 5;

    color: white;

    font-size: 13px;

    font-weight: 800;

    text-align: center;

    padding: 10px 5px 8px;

    min-height: 43px;

    display: flex;

    align-items: center;

    justify-content: center;

    text-shadow:
        0 0 8px rgba(255,255,255,0.12);
}


/* ============================================================
   DETAILS PAGE
   ============================================================ */

.details-title {

    font-size: clamp(30px, 5vw, 55px);

    font-weight: 950;

    margin-top: 25px;

    margin-bottom: 20px;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #00aaff,
            #9d00ff,
            #ff0066
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    background-clip: text;
}

.trailer-heading {

    font-size: 32px;

    font-weight: 950;

    margin-top: 15px;

    margin-bottom: 15px;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #00aaff,
            #9d00ff,
            #ff0066
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    background-clip: text;
}

.trailer-box {

    width: 100%;

    padding: 4px;

    border-radius: 18px;

    background:
        linear-gradient(
            90deg,
            #006cff,
            #00c8ff,
            #8b00ff,
            #ff0066,
            #ff1744
        );

    box-shadow:
        0 0 20px rgba(0,110,255,0.55),
        0 0 35px rgba(255,0,80,0.45);

    margin-bottom: 35px;
}

.trailer-inner {

    width: 100%;

    border-radius: 14px;

    overflow: hidden;

    background: #000;
}

.center-poster-wrap {

    width: 100%;

    aspect-ratio: 16 / 9;

    margin: 25px auto 35px;

    padding: 4px;

    border-radius: 18px;

    background:
        linear-gradient(
            90deg,
            #006cff,
            #00c8ff,
            #8b00ff,
            #ff0066,
            #ff1744
        );

    box-shadow:
        0 0 20px rgba(0,110,255,0.55),
        0 0 35px rgba(255,0,80,0.45);

    overflow: hidden;
}

.center-poster {

    width: 100%;
    height: 100%;

    aspect-ratio: 16 / 9;

    object-fit: cover;

    display: block;

    border-radius: 14px;
}

.details-panel {

    position: relative;

    padding: 28px;

    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            rgba(0,20,50,0.78),
            rgba(15,5,30,0.78),
            rgba(50,0,25,0.70)
        );

    border: 2px solid transparent;

    background-clip: padding-box;

    box-shadow:
        0 0 20px rgba(0,110,255,0.35),
        0 0 35px rgba(255,0,70,0.25);

    overflow: hidden;
}

.details-panel::before {

    content: "";

    position: absolute;

    inset: 0;

    padding: 2px;

    border-radius: 20px;

    background:
        linear-gradient(
            90deg,
            #006cff,
            #00c8ff,
            #9d00ff,
            #ff0066,
            #ff1744,
            #006cff
        );

    background-size: 300% 100%;

    animation: neonBorder 4s linear infinite;

    -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);

    -webkit-mask-composite: xor;

    mask-composite: exclude;

    pointer-events: none;
}

.info-heading {

    font-size: 30px;

    font-weight: 950;

    color: white;

    margin-bottom: 22px;
}

.info-grid {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 18px;

    margin-bottom: 25px;
}

.info-item {

    padding: 18px;

    border-radius: 14px;

    background:
        linear-gradient(
            135deg,
            rgba(0,80,180,0.15),
            rgba(255,0,80,0.12)
        );

    border:
        1px solid rgba(0,160,255,0.35);

    box-shadow:
        0 0 12px rgba(0,110,255,0.12);
}

.info-label {

    color: #aeb4c5;

    font-size: 13px;

    margin-bottom: 6px;
}

.info-value {

    color: white;

    font-size: 20px;

    font-weight: 850;
}

.genre-section,
.story-section {

    padding-top: 20px;

    margin-top: 18px;

    border-top:
        1px solid rgba(0,150,255,0.35);
}

.genre-title,
.story-title {

    font-size: 20px;

    font-weight: 900;

    color: white;

    margin-bottom: 10px;
}

.genre-tag {

    display: inline-block;

    padding: 7px 15px;

    margin: 4px 5px 4px 0;

    border-radius: 50px;

    color: white;

    border: 1px solid #008cff;

    background:
        linear-gradient(
            90deg,
            rgba(0,110,255,0.20),
            rgba(150,0,255,0.20)
        );

    box-shadow:
        0 0 10px rgba(0,110,255,0.25);
}

.story-text {

    color: #c5cad5;

    line-height: 1.8;

    font-size: 15px;
}


/* ============================================================
   TEAM FOOTER
   ============================================================ */

.team-footer {

    position: relative;

    width: 100%;

    margin-top: 45px;

    padding: 0 12px 35px;

    text-align: center;

    overflow: hidden;
}

.team-neon-line {

    width: 82%;

    height: 3px;

    margin: 0 auto 30px;

    background:
        linear-gradient(
            90deg,
            transparent 0%,
            #006cff 18%,
            #00c8ff 35%,
            #9d00ff 50%,
            #ff0066 68%,
            #006cff 84%,
            transparent 100%
        );

    box-shadow:
        0 0 8px #006cff,
        0 0 15px #9d00ff,
        0 0 20px #ff0066;

    border-radius: 50%;

    animation: teamLineGlow 3s ease-in-out infinite;
}

@keyframes teamLineGlow {

    0% {
        opacity: 0.75;
        transform: scaleX(0.96);
    }

    50% {
        opacity: 1;
        transform: scaleX(1);
    }

    100% {
        opacity: 0.75;
        transform: scaleX(0.96);
    }
}

.team-grid {

    width: 92%;

    max-width: 1150px;

    margin: 0 auto;

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    align-items: stretch;
}

.team-member {

    min-height: 150px;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    padding: 8px 12px;

    position: relative;
}

.team-member + .team-member {

    border-left:
        1px solid
        rgba(100, 120, 160, 0.35);
}


/* ============================================================
   ANISH PHOTO
   ============================================================ */

.team-photo {

    width: 62px;

    height: 62px;

    border-radius: 50%;

    object-fit: cover;

    object-position: center;

    padding: 3px;

    margin-bottom: 8px;

    background:
        linear-gradient(
            135deg,
            #ff00ff,
            #7b00ff,
            #00aaff,
            #ff0066
        );

    box-shadow:
        0 0 8px #ff00ff,
        0 0 18px rgba(255,0,255,0.75),
        0 0 30px rgba(0,140,255,0.45);

    animation:
        profileGlow 2.5s ease-in-out infinite;
}

@keyframes profileGlow {

    0% {

        transform: scale(1);

        box-shadow:
            0 0 8px #ff00ff,
            0 0 18px rgba(255,0,255,0.60);
    }

    50% {

        transform: scale(1.05);

        box-shadow:
            0 0 12px #ff00ff,
            0 0 25px rgba(255,0,255,0.90),
            0 0 35px rgba(0,140,255,0.50);
    }

    100% {

        transform: scale(1);

        box-shadow:
            0 0 8px #ff00ff,
            0 0 18px rgba(255,0,255,0.60);
    }
}


/* ============================================================
   TEAM ICONS
   ============================================================ */

.team-icon {

    height: 38px;

    display: flex;

    align-items: center;

    justify-content: center;

    margin-bottom: 8px;

    font-size: 29px;

    font-weight: 950;

    line-height: 1;
}

.icon-math {

    color: #00ff95;

    text-shadow:
        0 0 8px #00ff95,
        0 0 16px rgba(0,255,149,0.65);
}

.icon-project {

    color: #00bfff;

    text-shadow:
        0 0 8px #00bfff,
        0 0 16px rgba(0,191,255,0.7);
}

.icon-front {

    color: #ffd000;

    text-shadow:
        0 0 8px #ffd000,
        0 0 16px rgba(255,208,0,0.65);
}


/* ============================================================
   TEAM TEXT
   ============================================================ */

.team-role {

    color: #f4f4f8;

    font-size: 13px;

    font-weight: 650;

    line-height: 1.35;

    min-height: 35px;

    display: flex;

    align-items: center;

    justify-content: center;

    text-align: center;
}

.team-name {

    margin-top: 5px;

    font-size: 17px;

    font-weight: 900;

    line-height: 1.2;

    white-space: nowrap;
}

.name-anish {

    color: #ff39ff;

    text-shadow:
        0 0 8px rgba(255,57,255,0.55);
}

.name-abhishek {

    color: #00f58a;

    text-shadow:
        0 0 8px rgba(0,245,138,0.5);
}

.name-abrar {

    color: #00aaff;

    text-shadow:
        0 0 8px rgba(0,170,255,0.55);
}

.name-vishal {

    color: #ffd000;

    text-shadow:
        0 0 8px rgba(255,208,0,0.55);
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    .block-container {
        padding-left: 10px;
        padding-right: 10px;
    }

    .hero-box {

        min-height: 300px;

        padding: 28px 24px;

        border-radius: 15px;
    }

    .hero-title {

        font-size: 42px;

        line-height: 1;
    }

    .selected-movie-box {

        gap: 15px;

        padding: 12px;

        min-height: 145px;
    }

    .selected-poster {

        width: 85px;

        height: 125px;
    }

    .selected-title {

        font-size: 24px;
    }

    .selected-overview {

        font-size: 12px;

        line-height: 1.45;

        display: -webkit-box;

        -webkit-line-clamp: 4;

        -webkit-box-orient: vertical;

        overflow: hidden;
    }

    .section-title {

        font-size: 25px;
    }

    .movie-wrapper {

        border-radius: 11px;

        padding: 4px;

        margin-bottom: 12px;
    }

    .movie-wrapper:hover {

        transform:
            translateY(-4px)
            scale(1.015);
    }

    .movie-title {

        font-size: 10px;

        min-height: 36px;

        padding: 7px 3px;
    }

    .play-circle {

        width: 44px;

        height: 44px;

        font-size: 18px;
    }

    div[data-testid="stHorizontalBlock"] {

        padding: 4px 2px;

        border-radius: 12px;

        margin-bottom: 5px;
    }

    .trailer-box {

        padding: 3px;

        border-radius: 14px;
    }

    .trailer-inner {

        border-radius: 11px;
    }

    .trailer-heading {

        font-size: 25px;
    }

    .center-poster-wrap {

        width: 100%;

        aspect-ratio: 16 / 9;

        margin: 20px auto 30px;

        padding: 3px;

        border-radius: 14px;
    }

    .center-poster {

        width: 100%;

        height: 100%;

        object-fit: cover;

        border-radius: 11px;
    }

    .details-panel {

        padding: 18px;
    }

    .info-grid {

        grid-template-columns: 1fr;
    }

    .info-value {

        font-size: 18px;
    }


    /* ============================================
       MOBILE FOOTER
       ============================================ */

    .team-footer {

        margin-top: 35px;

        padding: 0 4px 25px;
    }

    .team-neon-line {

        width: 88%;

        height: 2px;

        margin-bottom: 20px;
    }

    .team-grid {

        width: 100%;

        grid-template-columns:
            repeat(4, 1fr);
    }

    .team-member {

        min-height: 135px;

        padding: 5px 4px;
    }

    .team-member + .team-member {

        border-left:
            1px solid
            rgba(100, 120, 160, 0.30);
    }

    .team-photo {

        width: 45px;

        height: 45px;

        padding: 2px;

        margin-bottom: 5px;
    }

    .team-icon {

        height: 29px;

        font-size: 22px;

        margin-bottom: 6px;
    }

    .team-role {

        font-size: 9px;

        line-height: 1.25;

        min-height: 31px;
    }

    .team-name {

        margin-top: 5px;

        font-size: 11px;
    }
}

</style>
""")


# ============================================================
# 3. FILE PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MOVIES_FILE = os.path.join(
    BASE_DIR,
    "movies.pkl"
)

SIMILARITY_FILE = os.path.join(
    BASE_DIR,
    "similarity.pkl.gz"
)


# ============================================================
# 4. ANISH PHOTO URL
# ============================================================

ANISH_PHOTO_URL = (
    "https://i.ibb.co/PsGGDLyW/"
    "IMG-20260920-084857-1.png"
)


# ============================================================
# 5. LOAD DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_data():

    with open(
        MOVIES_FILE,
        "rb"
    ) as file:

        movies_data = pickle.load(file)


    with gzip.open(
        SIMILARITY_FILE,
        "rb"
    ) as file:

        similarity_data = pickle.load(file)


    return (
        movies_data,
        similarity_data["indices"]
    )


movies, similarity_indices = load_data()


# ============================================================
# 6. TMDB API KEY
# ============================================================

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]


# ============================================================
# 7. TMDB REQUEST
# ============================================================

def tmdb_request(
    endpoint,
    params=None
):

    url = (
        "https://api.themoviedb.org/3/"
        + endpoint
    )


    if params is None:

        params = {}


    params = params.copy()

    params["api_key"] = TMDB_API_KEY


    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )


        if response.status_code == 200:

            return response.json()


    except Exception:

        return None


    return None


# ============================================================
# 8. MOVIE DETAILS
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_movie_details(movie_id):

    return tmdb_request(
        f"movie/{movie_id}",
        {
            "language": "en-US"
        }
    )


# ============================================================
# 9. POSTER
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_poster(movie_id):

    details = fetch_movie_details(
        movie_id
    )


    if not details:

        return None


    poster_path = details.get(
        "poster_path"
    )


    if not poster_path:

        return None


    return (
        "https://image.tmdb.org/t/p/w500"
        + poster_path
    )


# ============================================================
# 10. TRAILER
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_trailer(movie_id):

    data = tmdb_request(
        f"movie/{movie_id}/videos",
        {
            "language": "en-US"
        }
    )


    if not data:

        return None


    videos = data.get(
        "results",
        []
    )


    # OFFICIAL TRAILER
    for video in videos:

        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
            and video.get("official") is True
        ):

            key = video.get("key")

            if key:

                return (
                    "https://www.youtube.com/watch?v="
                    + key
                )


    # NORMAL TRAILER
    for video in videos:

        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
        ):

            key = video.get("key")

            if key:

                return (
                    "https://www.youtube.com/watch?v="
                    + key
                )


    # TEASER
    for video in videos:

        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Teaser"
        ):

            key = video.get("key")

            if key:

                return (
                    "https://www.youtube.com/watch?v="
                    + key
                )


    return None


# ============================================================
# 11. RECOMMENDATION
# ============================================================

def recommend(movie):

    indexes = movies[
        movies["title"] == movie
    ].index


    if len(indexes) == 0:

        return [], [], []


    index = indexes[0]


    names = []
    posters = []
    ids = []


    similar_movies = (
        similarity_indices[index][0:20]
    )


    for movie_index in similar_movies:

        try:

            movie_index = int(
                movie_index
            )

        except Exception:

            continue


        try:

            movie_id = movies.iloc[
                movie_index
            ]["movie_id"]

            movie_name = movies.iloc[
                movie_index
            ]["title"]

        except Exception:

            continue


        names.append(
            movie_name
        )

        posters.append(
            fetch_poster(movie_id)
        )

        ids.append(
            movie_id
        )


    return (
        names,
        posters,
        ids
    )


# ============================================================
# 12. MOVIE CARD
# ============================================================

def movie_card_html(
    movie_name,
    poster_url,
    movie_id
):

    safe_name = html.escape(
        str(movie_name)
    )


    if not poster_url:

        poster_url = (
            "https://via.placeholder.com/"
            "500x750?text=No+Poster"
        )


    return f"""
    <a
        href="?movie_id={movie_id}"
        target="_self"
        style="
            display:block;
            text-decoration:none;
            color:white;
        "
    >

        <div class="movie-wrapper">

            <div class="movie-poster-container">

                <img
                    class="movie-poster"
                    src="{poster_url}"
                    alt="{safe_name}"
                    loading="lazy"
                >

                <div class="movie-overlay">

                    <div class="play-circle">
                        ▶
                    </div>

                </div>

            </div>

            <div class="movie-title">
                {safe_name}
            </div>

        </div>

    </a>
    """


# ============================================================
# 13. SELECTED MOVIE PREVIEW
# ============================================================

def selected_movie_preview(
    movie_name
):

    indexes = movies[
        movies["title"] == movie_name
    ].index


    if len(indexes) == 0:

        return


    index = indexes[0]


    try:

        movie_id = movies.iloc[
            index
        ]["movie_id"]

    except Exception:

        return


    details = fetch_movie_details(
        movie_id
    )


    if not details:

        return


    poster_path = details.get(
        "poster_path"
    )

    overview = details.get(
        "overview",
        "No description available."
    )


    safe_title = html.escape(
        str(
            details.get(
                "title",
                movie_name
            )
        )
    )


    safe_overview = html.escape(
        str(overview)
    )


    if poster_path:

        poster_url = (
            "https://image.tmdb.org/t/p/w500"
            + poster_path
        )

    else:

        poster_url = (
            "https://via.placeholder.com/"
            "500x750?text=No+Poster"
        )


    st.html(
        f"""
        <div class="selected-movie-box">

            <img
                class="selected-poster"
                src="{poster_url}"
                alt="{safe_title}"
            >

            <div class="selected-info">

                <span class="selected-badge">
                    ⭐ Selected Movie
                </span>

                <div class="selected-title">
                    {safe_title}
                </div>

                <div class="selected-overview">
                    {safe_overview}
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# 14. DETAILS PAGE
# ============================================================

def show_movie_details(
    movie_id
):

    if st.button(
        "←  Back to Recommendations",
        key="back_button"
    ):

        st.query_params.clear()

        st.rerun()


    details = fetch_movie_details(
        movie_id
    )


    if not details:

        st.error(
            "Movie information could not be loaded."
        )

        return


    title = details.get(
        "title",
        "Unknown Movie"
    )

    overview = details.get(
        "overview",
        "No description available."
    )

    rating = details.get(
        "vote_average",
        0
    )

    release_date = details.get(
        "release_date",
        "Unknown"
    )

    runtime = details.get(
        "runtime",
        0
    )

    genres = details.get(
        "genres",
        []
    )

    poster_path = details.get(
        "poster_path"
    )


    # TRAILER

    st.html(
        '<div class="trailer-heading">'
        '▶️ Trailer'
        '</div>'
    )


    trailer_url = fetch_trailer(
        movie_id
    )


    if trailer_url:

        st.html(
            '<div class="trailer-box">'
            '<div class="trailer-inner">'
        )

        st.video(
            trailer_url
        )

        st.html(
            "</div></div>"
        )

    else:

        st.warning(
            "🎬 Trailer is not available for this movie."
        )


    # POSTER

    if poster_path:

        poster_url = (
            "https://image.tmdb.org/t/p/w780"
            + poster_path
        )


        st.html(
            f"""
            <div class="center-poster-wrap">

                <img
                    class="center-poster"
                    src="{poster_url}"
                    alt="{html.escape(str(title))}"
                >

            </div>
            """
        )


    # TITLE

    st.html(
        f"""
        <div class="details-title">

            🎬 {html.escape(str(title))}

        </div>
        """
    )


    # RUNTIME

    runtime_text = "Unknown"


    if runtime:

        hours = runtime // 60

        minutes = runtime % 60


        if hours:

            runtime_text = (
                f"{hours}h {minutes}min"
            )

        else:

            runtime_text = (
                f"{minutes}min"
            )


    # GENRES

    genre_html = ""


    for genre in genres:

        genre_name = genre.get(
            "name"
        )


        if genre_name:

            genre_html += (
                '<span class="genre-tag">'
                f'{html.escape(str(genre_name))}'
                '</span>'
            )


    safe_overview = html.escape(
        str(overview)
    )


    # DETAILS PANEL

    st.html(
        f"""
        <div class="details-panel">

            <div class="info-heading">

                🎬 {html.escape(str(title))}

            </div>


            <div class="info-grid">


                <div class="info-item">

                    <div class="info-label">
                        ⭐ TMDB Rating
                    </div>

                    <div class="info-value">
                        {float(rating):.1f}/10
                    </div>

                </div>


                <div class="info-item">

                    <div class="info-label">
                        📅 Release Date
                    </div>

                    <div class="info-value">
                        {html.escape(
                            str(release_date)
                        )}
                    </div>

                </div>


                <div class="info-item">

                    <div class="info-label">
                        ⏱️ Runtime
                    </div>

                    <div class="info-value">
                        {html.escape(
                            str(runtime_text)
                        )}
                    </div>

                </div>


            </div>


            <div class="genre-section">

                <div class="genre-title">
                    🎭 Genres
                </div>

                <div>
                    {genre_html}
                </div>

            </div>


            <div class="story-section">

                <div class="story-title">
                    📝 Story
                </div>

                <div class="story-text">
                    {safe_overview}
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# 15. QUERY PARAMETER
# ============================================================

movie_id_from_url = st.query_params.get(
    "movie_id"
)


# ============================================================
# 16. DETAILS PAGE
# ============================================================

if movie_id_from_url:

    try:

        movie_id = int(
            movie_id_from_url
        )

        show_movie_details(
            movie_id
        )

    except (
        ValueError,
        TypeError
    ):

        st.error(
            "Invalid movie ID."
        )


# ============================================================
# 17. MAIN PAGE
# ============================================================

else:

    # ========================================================
    # HERO
    # ========================================================

    st.html(
        """
        <div class="hero-box">

            <div class="hero-content">

                <div
                    style="
                        color:#ff1744;
                        font-size:13px;
                        font-weight:900;
                        letter-spacing:3px;
                    "
                >

                    🎬 DEVELOPED BY
                    ANISH-ABRAR-ABHISHEK-VISHAL

                </div>


                <div class="hero-title">

                    Movie

                    <br>

                    <span class="gradient-text">
                        Recommendation
                    </span>

                    <br>

                    System

                </div>


                <div
                    style="
                        color:#c5cad5;
                        font-size:17px;
                        line-height:1.6;
                        max-width:650px;
                    "
                >

                    Discover movies similar to your
                    favourite movies using
                    AI-powered recommendations.

                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # CHOOSE MOVIE
    # ========================================================

    st.html(
        """
        <div
            style="
                font-size:32px;
                font-weight:900;
                margin-bottom:8px;
            "
        >

            🎬

            <span style="color:white;">
                Choose
            </span>

            <span
                style="
                    background:
                        linear-gradient(
                            90deg,
                            #00aaff,
                            #9d00ff,
                            #ff0066
                        );

                    -webkit-background-clip:text;
                    -webkit-text-fill-color:transparent;
                "
            >

                Your Movie

            </span>

        </div>
        """
    )


    movie_list = (
        movies["title"]
        .dropna()
        .values
    )


    default_index = 0


    if "Avatar" in movie_list:

        default_index = list(
            movie_list
        ).index("Avatar")


    selected_movie = st.selectbox(
        "Choose movie",
        movie_list,
        index=default_index,
        key="movie_selector"
    )


    selected_movie_preview(
        selected_movie
    )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    names, posters, ids = recommend(
        selected_movie
    )


    st.html(
        f"""
        <div class="section-title">

            🔥 Recommended Movies

        </div>

        <div class="section-subtitle">

            Because you selected

            <strong
                style="
                    color:#00aaff;
                    text-shadow:
                        0 0 8px
                        rgba(0,170,255,0.6);
                "
            >

                {html.escape(
                    str(selected_movie)
                )}

            </strong>

            <br>

            👆 Tap any poster to open
            movie details

        </div>
        """
    )


    # ========================================================
    # MOVIE GRID
    # ========================================================

    COLS_PER_ROW = 5


    for row_start in range(
        0,
        len(names),
        COLS_PER_ROW
    ):

        cols = st.columns(
            COLS_PER_ROW,
            gap="medium"
        )


        for j in range(
            COLS_PER_ROW
        ):

            position = (
                row_start + j
            )


            if position >= len(names):

                continue


            with cols[j]:

                st.html(
                    movie_card_html(
                        names[position],
                        posters[position],
                        ids[position]
                    )
                )


    # ========================================================
    # TEAM FOOTER
    # ========================================================

    st.html(
        f"""
        <div class="team-footer">

            <div class="team-neon-line"></div>


            <div class="team-grid">


                <!-- ANISH -->

                <div class="team-member">

                    <img
                        class="team-photo"
                        src="{ANISH_PHOTO_URL}"
                        alt="Anish Kumar"
                        loading="lazy"
                    >


                    <div class="team-role">

                        Coding development<br>
                        by

                    </div>


                    <div class="team-name name-anish">

                        Anish Kumar

                    </div>

                </div>


                <!-- ABHISHEK -->

                <div class="team-member">

                    <div class="team-icon icon-math">

                        ▦

                    </div>


                    <div class="team-role">

                        Mathematical<br>
                        calculation by

                    </div>


                    <div class="team-name name-abhishek">

                        Abhishek Kumar

                    </div>

                </div>


                <!-- ABRAR -->

                <div class="team-member">

                    <div class="team-icon icon-project">

                        ☁

                    </div>


                    <div class="team-role">

                        Manage project by

                    </div>


                    <div class="team-name name-abrar">

                        Abrar Ahmad

                    </div>

                </div>


                <!-- VISHAL -->

                <div class="team-member">

                    <div class="team-icon icon-front">

                        ▱

                    </div>


                    <div class="team-role">

                        Front development by

                    </div>


                    <div class="team-name name-vishal">

                        Vishal Kumar

                    </div>

                </div>


            </div>

        </div>
        """
    )