---
name: Warm Neumorphism
colors:
  surface: '#fdf9f1'
  surface-dim: '#dddad2'
  surface-bright: '#fdf9f1'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f7f3eb'
  surface-container: '#f2ede5'
  surface-container-high: '#ece8e0'
  surface-container-highest: '#e6e2da'
  on-surface: '#1c1c17'
  on-surface-variant: '#45474b'
  inverse-surface: '#31302b'
  inverse-on-surface: '#f4f0e8'
  outline: '#75777b'
  outline-variant: '#c5c6cb'
  surface-tint: '#5a5f66'
  primary: '#171c23'
  on-primary: '#ffffff'
  primary-container: '#2c3138'
  on-primary-container: '#9499a1'
  inverse-primary: '#c2c7d0'
  secondary: '#585f6c'
  on-secondary: '#ffffff'
  secondary-container: '#dce2f3'
  on-secondary-container: '#5e6572'
  tertiary: '#002118'
  on-tertiary: '#ffffff'
  tertiary-container: '#00382b'
  on-tertiary-container: '#65a58f'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dee3ec'
  primary-fixed-dim: '#c2c7d0'
  on-primary-fixed: '#171c22'
  on-primary-fixed-variant: '#42474f'
  secondary-fixed: '#dce2f3'
  secondary-fixed-dim: '#c0c7d6'
  on-secondary-fixed: '#151c27'
  on-secondary-fixed-variant: '#404754'
  tertiary-fixed: '#aef0d7'
  tertiary-fixed-dim: '#93d4bc'
  on-tertiary-fixed: '#002118'
  on-tertiary-fixed-variant: '#04513f'
  background: '#fdf9f1'
  on-background: '#1c1c17'
  surface-variant: '#e6e2da'
typography:
  headline-xl:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.03em
  headline-xl-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 36px
    fontWeight: '600'
    lineHeight: 44px
    letterSpacing: -0.025em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '600'
    lineHeight: 34px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0em
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0.005em
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1.5rem
  margin: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system expresses a serene, tactile, and sculptured digital environment. It merges the physical intuition of soft-molded architectural materials—such as warm alabaster, bone china, and matte limestone—with contemporary ergonomic digital interactions. The aesthetic rejects harsh borders, plastic gloss, and planar flat surfaces in favor of continuous volumetric planes that appear extruded directly from the substrate canvas.

The target audience encompasses discerning professionals and luxury-tier product users seeking calm, tactile reassurance, reduced optical fatigue, and organic digital craftsmanship. Every control feels sculpted, weighted, and responsive, evoking precision-milled industrial design and high-end physical haptics.

## Colors

The palette is rooted in light, organic warmth. The canvas substrate is an unbleached warm bone clay (`#ebe7df`), providing a radiant yet glare-free foundation. Surfacing variations blend subtly toward soft pale chalk (`#f4f1ea`) and deeper pressed clay (`#dfdad0`).

- **Canvas & Substrate (`#ebe7df`):** The primary neutral plane from which all extruded elements emerge and into which sunken elements recede. Elements share this background tone to maintain volumetric illusion.
- **Sculpting Highlight (`#ffffff` at 70%–85% opacity):** Cast from an overhead top-left light angle (315°), lending crisp surface definition to raised rims.
- **Sculpting Shadow (`#c7c0b3` and `#1a1e24` at 6%–18% opacity):** Dispersed beneath bottom-right bevels to yield soft, tangible lift.
- **Primary Ink (`#2c3138`):** Deep basalt slate used for primary legibility, avoiding harsh pure black while maintaining rigorous WCAG AAA contrast against the bone canvas.
- **Secondary Ink (`#6b7280`):** Muted stone gray for tertiary descriptors, captions, and deactivated glyphs.
- **Muted Semantic Status Accents:**
  - *Clinical Sage / Emerald (`#387864`):* Affirmation, success, and positive balances.
  - *Muted Coral Rose (`#c45b53`):* Alerts, destructive triggers, and negative indicators.
  - *Warm Amber Mineral (`#c98a3b`):* Warnings, ratings, stars, and active badges.

## Typography

The design system employs **Plus Jakarta Sans** uniformly across all tiers. Its geometry provides clean legibility that balances the physical soft shadows and curves of the interface without appearing overly technical. 

- Large display headlines utilize heavier weights (`700`, `600`) with tightened tracking to ground floating sections.
- Body copy relies on generous vertical rhythm (`1.5` to `1.6` line-height multiples) to provide breathing room and prevent dense text from disrupting the extruded illusion.
- Labels and control microcopy use medium-to-bold weights with slight tracking expansion to maintain optical clarity on contoured pill buttons and recessed wells.

## Layout & Spacing

Tactile extrusion requires expansive negative space; without ample breathing room, adjoining dual-directional shadows collide and break the visual relief. 

- **Grid Architecture:** 12-column adaptive fluid grid on desktop (`>1024px`) with `2.5rem` section margins and `1.5rem` gutters. Tablet devices (`768px–1023px`) scale to an 8-column layout with `1.5rem` margins and `1rem` gutters. Mobile viewports (`<767px`) collapse to a 4-column flow with `1rem` margins and gutters.
- **Component Padding Scale:**
  - `space-xs` (4px): Micro-spacing between paired inline badges and icons.
  - `space-sm` (8px): Internal gaps between chips, list metadata, and sub-items.
  - `space-md` (16px): Compact button padding, input field interiors, and standard card insets.
  - `space-lg` (24px): Standard card container padding and module grouping distance.
  - `space-xl` (40px): Section margins, macro-card padding, and volumetric card separation.

## Elevation & Depth

All physical depth in this design system is created via a single unified light vector originating from the top-left at 315° (top: -1, left: -1). Surface colors match or closely follow the background substrate (`#ebe7df`). Depth is articulated through paired directional illumination:

1. **Extruded Convex (Elevated / Floating Elements):**
   - *Drop Highlight:* `-8px -8px 16px rgba(255, 255, 255, 0.9), -2px -2px 4px rgba(255, 255, 255, 0.4)`
   - *Drop Shadow:* `8px 8px 18px rgba(184, 177, 166, 0.45), 2px 2px 5px rgba(184, 177, 166, 0.25)`
   - Applied to interactive buttons, active cards, floating chips, and toggles in their resting state.

2. **Sunken Concave (Recessed / Inset Wells):**
   - *Inset Shadow:* `inset 4px 4px 8px rgba(184, 177, 166, 0.45), inset -4px -4px 8px rgba(255, 255, 255, 0.85)`
   - Applied to text inputs, progress grooves, unselected radio troughs, and depressed button states.

3. **Flat Neutral (Surface Planes):**
   - Elements at `elevation-0` share zero offset and use pure negative space rather than divider lines or borders to define spatial hierarchy.

## Shapes

The shape grammar relies on deep radii, organic transitions, and elongated pill silhouettes. Sharp 90-degree corners are strictly avoided; hard angles shatter the continuous clay-surface illusion.

- **Primary Geometry:** Full pill closures (`9999px` / `rounded-full`) for all standard buttons, search wells, chips, segmented tabs, and floating triggers.
- **Panel Containers:** Substantial curvature matching `rounded-2xl` to `rounded-3xl` (18px to 28px). Internal corner radii follow nested concentric curves ($R_{outer} - Padding = R_{inner}$) to preserve structural alignment.

## Components

### Buttons & Interactive Controls
- **Resting State:** Extruded dual-shadow treatment on a background matching `#ebe7df`. Full pill shape. Text rendered in `#2c3138`.
- **Hover State:** Shadow blur expands by 25% while maintaining directional coordinate vectors, visually floating closer to the user.
- **Active / Pressed State:** Shifts instantly to an inset dual shadow (`inset 3px 3px 6px ...`), visually compressing into the substrate plane.
- **Primary Accent Pill:** Subtle warm clay tint with the same dual shadows, utilizing a muted sage or warm amber icon glyph for focal hierarchy.

### Input Fields
- **Container:** Continuously recessed sunken well (`inset 4px 4px 8px ...`). Pill or 18px radius.
- **Text & Placeholder:** Input text set in primary slate `#2c3138`; placeholder set in secondary stone `#6b7280`.
- **Focus State:** Inset shadow warms slightly, complemented by a soft, diffused 1px perimeter glow in muted sage (`#387864` at 40% opacity).

### Chips & Segmented Controls
- **Track:** Sunken pill well running behind the controls.
- **Selected Chip:** Raised extruded pill that appears to slide across the recessed bed.
- **Unselected Chip:** Flush against the recess, rendered in `#6b7280` text without drop shadows.

### Checkboxes & Radio Buttons
- **Radio Buttons:** Outer circle (24px) styled as a deep sunken basin. Selected state places an extruded floating central pebble or a muted emerald pearl within the basin.
- **Checkboxes:** Rounded-lg (8px) sunken cavity. Checked state displays an embossed checkmark in muted sage green.

### Cards & Grouping Vessels
- Generous outer margins with 24px–28px radius. Dual ambient extrusion with light top-left perimeter sheen. No dividing border strokes. Content sections within the card are separated by whitespace or gentle counter-sunken wells.

### Status Indicators & Badges
- Small extruded pill tags housing muted clinical tones: emerald green for confirmations, coral rose for critical alerts, and warm mineral amber for warnings. Badges feature matching soft tinted text against bone backgrounds.