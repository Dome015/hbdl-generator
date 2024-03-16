# hbdl-generator
A synthetic image-to-html dataset generator.

## Layout
The layout is randomly generated using css flexbox styling attributes. A page has a sequence of rows, and each row is made up by a sequence of columns.
Each column can have custom styling, which is different from the rest of the page, and will contain a block.

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