# Genesis Family Camping

Static site, no server, no database. **`data/trips.json` is the only file
you should ever edit.** Everything else — the homepage timeline, each trip's
detail page — is generated from it by `build.py`, and GitHub Actions rebuilds
the whole site automatically:

- every time you push a change, **and**
- once a day on its own (9am UTC), so a trip quietly drops off the homepage
  timeline the moment its date passes — you never have to remove it by hand.

The generated `index.html` / `trips/*.html` aren't committed to git (see
`.gitignore`) — they're a build output, regenerated fresh every time, so
there's nothing to hand-edit and nothing to drift out of sync with the
template. If you ever do want to change the design (colors, copy, layout),
that lives in `build.py`, in one place, and every page updates consistently
the next time it builds.

## One-time setup

1. **Install Claude Code** (if you haven't): https://docs.claude.com/en/docs/claude-code/overview
   Either the native installer, or `npm install -g @anthropic-ai/claude-code`.

2. **Create a GitHub repo** (on github.com): click "New repository," name it
   something like `genesis-camping`, keep it Public (required for free GitHub
   Pages on a personal account), don't add a README/gitignore (we already have
   files).

3. **Push this folder to it.** From inside this folder:
   ```
   git init
   git add .
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/<your-username>/genesis-camping.git
   git push -u origin main
   ```

4. **Turn on Pages.** In the GitHub repo: Settings → Pages → under "Build and
   deployment," set Source to **GitHub Actions**. The included workflow
   (`.github/workflows/deploy.yml`) builds the site fresh from
   `data/trips.json` and publishes it automatically. First deploy takes a
   minute or two; your site will be live at
   `https://<your-username>.github.io/genesis-camping/`.

5. **Optional: custom domain.** Settings → Pages → Custom domain, then add a
   `CNAME` record at your DNS provider pointing to `<your-username>.github.io`.

## Adding a new trip (the normal workflow)

Open a terminal in this project folder and run `claude` to start Claude Code.
Then just describe the trip in plain language, e.g.:

> Add a new trip to data/trips.json: Manatee Hammock, October 10 2026,
> group site booked through our Square page at [url]. It's a shaded
> 26-acre campground near Kennedy Space Center with a pool, pavilion,
> shuffleboard and pickleball courts. Then push it.

Claude Code will add an entry to `data/trips.json` (matching the shape of
the existing ones, including `date_iso` in `YYYY-MM-DD` format — that's what
drives the "still upcoming" filtering) and push it. GitHub Actions rebuilds
and deploys automatically — you don't need to run anything locally, and you
never touch HTML.

You can also do it by hand: edit `data/trips.json`, `git add . && git commit
-m "Add <trip name>" && git push`.

### Previewing before you push (optional)

If you want to see the result before pushing:
```
python3 build.py
open index.html      # or just double-click it
```
These generated files aren't tracked by git (see above), so previewing
locally never risks accidentally committing a stray edit to the HTML.

## Adding a photo to a trip

Drop the image at `assets/images/trips/<slug>.jpg`, then set
`"photo": "assets/images/trips/<slug>.jpg"` on that trip in `data/trips.json`
and push. Until a photo is set, the card/page shows a placeholder.

## File map

```
data/trips.json          <- edit this to add/change/remove trips (source of truth)
build.py                 <- generates the HTML from trips.json (design lives here)
assets/images/            hero.jpg, host.jpg, icon.png, trips/*.jpg
.github/workflows/deploy.yml   rebuilds + publishes on push AND daily
index.html, trips/*.html   <- generated locally by build.py, gitignored, never edited by hand
```

