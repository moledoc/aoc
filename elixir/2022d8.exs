defmodule Solution do

  def tmp(line) do
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

  # def merge_mat(a, b, rows, cols) do
  #     Enum.zip(fwd, bwd) 
  #     |> Enum.map(fn({f,b}) -> f+b > 0 && 1 || 0 end)
  # end

  def ex1(filename) do
    content = File.read!(filename)
    |> String.trim("\n")
    |> String.split("\n")
    |> Enum.map(fn(x) -> 
      String.split(x, "")
      |> Enum.filter(fn(x) -> x != "" end)
      |> Enum.map(fn(x) -> 
        String.to_integer(x)
        # case x do
        #   "" -> 0
        #   _ -> String.to_integer(x) 
        # end
      end)
    end)

    # zeroes = content
    # |> Enum.take(1)
    # |> List.flatten
    # |> Enum.map(fn(_x) -> 0 end)

    # content = content
    # |> List.insert_at(-1, zeroes)
    # |> List.insert_at(0, zeroes)

    row_count = length(content)
    col_count = content
    |> Enum.at(0)
    |> length

    rows = for row <- 0..(row_count-1) do
      fwd = content |> Enum.at(row) |> tmp
      bwd = content |> Enum.at(row) |> Enum.reverse |> tmp |> Enum.reverse

      Enum.zip(fwd, bwd) 
      |> Enum.map(fn({f,b}) -> f+b > 0 && 1 || 0 end)
    end 

    cols = for col <- 0..(col_count-1) do
      col_line = for row <- 0..(row_count-1) do
        content |> Enum.at(row) |> Enum.at(col)
      end
      fwd = col_line |> tmp
      bwd = col_line |> Enum.reverse |> tmp |> Enum.reverse

      Enum.zip(fwd, bwd) 
      |> Enum.map(fn({f,b}) -> f+b > 0 && 1 || 0 end)
    end

    # cols_t = transpose(cols, col_count, row_count)


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

end

IO.write("ex1: #{Solution.ex1("input.txt")}\n")
# IO.write("ex2: #{Solution.ex2("tmp.txt")}\n")
