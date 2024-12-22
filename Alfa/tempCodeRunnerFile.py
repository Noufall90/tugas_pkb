def main(win, width):
    ROWS = 31  # Keep the original 31x31 grid size
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Only allow placing start and end points
            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end and not spot.is_barrier():
                    start = spot
                    start.make_start()
                elif not end and spot != start and not spot.is_barrier():
                    end = spot
                    end.make_end()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if spot != start and spot != end and not spot.is_barrier():
                    spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start, end = None, None
                    grid = make_grid(ROWS, width)

                # Handle arrow key movements
                if start:
                    if event.key == pygame.K_UP:
                        start = move_start(grid, start, "UP")
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif event.key == pygame.K_DOWN:
                        start = move_start(grid, start, "DOWN")
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif event.key == pygame.K_LEFT:
                        start = move_start(grid, start, "LEFT")
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif event.key == pygame.K_RIGHT:
                        start = move_start(grid, start, "RIGHT")
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    
                    # Update visualization after movement
                    draw(win, grid, ROWS, width)

    pygame.quit()

main(WIN, WIDTH)