-- List all bands with Glam as their main style and rank by their longevity.
SELECT band_name, (2022 - formed) AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC;
