defmodule Solution do

  def one_hot_seen(line) do
    {_, collect} = Enum.reduce(line, {-1, []}, fn(x, {highest, collect}) -> 
      cond do
        highest < x-> {x, [1| collect]}
        true -> {highest, [0| collect]}
      end
    end)
    collect |> Enum.reverse
  end

  def transpose(mat, rows, cols) do
    for row <- 0..(rows-1) do
      for col <- 0..(cols-1) do
        mat |> Enum.at(col) |> Enum.at(row)
      end
    end
  end

  def ex1(filename) do
    content = File.read!(filename)
    |> String.trim("\n")
    |> String.split("\n")
    |> Enum.map(fn(x) -> 
      String.split(x, "")
      |> Enum.filter(fn(x) -> x != "" end)
      |> Enum.map(fn(x) -> 
        String.to_integer(x)
      end)
    end)

    row_count = length(content)
    col_count = content
    |> Enum.at(0)
    |> length

    rows = for row <- 0..(row_count-1) do
      fwd = content |> Enum.at(row) |> one_hot_seen
      bwd = content |> Enum.at(row) |> Enum.reverse |> one_hot_seen |> Enum.reverse

      Enum.zip(fwd, bwd) 
      |> Enum.map(fn({f,b}) -> f+b > 0 && 1 || 0 end)
    end 

    cols = for col <- 0..(col_count-1) do
      col_line = for row <- 0..(row_count-1) do
        content |> Enum.at(row) |> Enum.at(col)
      end
      fwd = col_line |> one_hot_seen
      bwd = col_line |> Enum.reverse |> one_hot_seen |> Enum.reverse

      Enum.zip(fwd, bwd) 
      |> Enum.map(fn({f,b}) -> f+b > 0 && 1 || 0 end)
    end

    merged = for row <- 0..(row_count-1) do
      for col <- 0..(col_count-1) do
        r = rows |> Enum.at(row) |> Enum.at(col)
        c = cols |> Enum.at(col) |> Enum.at(row)
        case {r, c} do
          {_, 1} -> 1
          {1, _} -> 1
          {0, 0} -> 0
        end
      end
    end

    merged
    |> Enum.reduce(0, fn(r, acc) -> 
      acc+(r |> Enum.reduce(0, fn(c, acc_c) -> acc_c+c end))
    end)
    # |> dbg
  end

  def safe_list(lst) do
    case lst do
      nil -> []
      _ -> lst
    end
  end

  def scenic(grid, lat, d_lat, lon, d_lon, target, acc) do

    {lat, lon} = cond do
      lat < 0 -> {nil, lon}
      lon < 0 -> {lat, nil}
      true -> {lat, lon}
    end
      
    val = case {lat, lon} do
      {nil, _lon} -> nil
      {_lat, nil} -> nil
      {lat, lon} -> Enum.at(grid, lat)
        |> safe_list
        |> Enum.at(lon)
    end

    cond do
      val == nil -> acc
      target <= val -> acc+1
      true -> scenic(grid, lat+d_lat, d_lat, lon+d_lon, d_lon, target, acc+1)
    end
  end

  def ex2(filename) do
    content = File.read!(filename)
    |> String.trim("\n")
    |> String.split("\n")
    |> Enum.map(fn(x) -> 
      String.split(x, "")
      |> Enum.filter(fn(x) -> x != "" end)
      |> Enum.map(fn(x) -> 
        String.to_integer(x)
      end)
    end)

    row_count = length(content)
    col_count = content
    |> Enum.at(0)
    |> length


    res = for row <- 0..(row_count-1) do
      for col <- 0..(col_count-1) do
        target = content |> Enum.at(row) |> Enum.at(col)
        score = scenic(content, row-1, -1, col, 0, target, 0)
          * scenic(content, row+1, 1, col, 0, target, 0)
          * scenic(content, row, 0, col+1, 1, target, 0)
          * scenic(content, row, 0, col-1, -1, target, 0)
        {row, col, score}
      end
    end


    {_, _, highest} = res
    |> List.flatten
    |> Enum.sort_by(fn({_,_,score})->score end, :desc)
    |> List.first

    highest
  end

end

IO.write("ex1: #{Solution.ex1("input.txt")}\n")
IO.write("ex2: #{Solution.ex2("input.txt")}\n")
