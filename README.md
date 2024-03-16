# Synthetic HTML dataset generator

## Main variables
- **html**: HTML code
- **css**: dictionary containing all css classes
- **left_pad**: current left padding

## Possible page structures
- Single large column
- Small left, large right column
- Large left, small right column

## Page CSS
A page has some CSS that is applied to all of it. It should affect:
- Font (not to be included in the initial draft)
- Text color
- Padding
- Background color
These styles are picked at the beginning of generation and applied to a root div.

## Page layout
A page can be laid out either as a single large column or as a combination of boxes.
Boxes can have their own styling, which can be consistent or not. 2-3 boxes per row.

## Possible blocks in column
- Form
- Table (large column only)
- Stand-alone button(s)
- Title (with optional paragraph)
- Text with button
- Text/value pairs

## Block CSS
- Text color
- Padding
- Background color
All are optional, otherwise inherited from the page.

## Layout


## Form
- Text color: main or custom one?

A form is composed of multiple form rows
A form row has the following variables:
- The labels are next or above the inputs?
- If the labels are above, how are they aligned?
- Are the labels bold?
- How many fields?
  - If labels above, up to 4; otherwise, up to 3

